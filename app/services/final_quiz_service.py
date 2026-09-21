from app.database.mongodb import get_database
from app.schemas.quiz import QuizPublic, QuizQuestionPublic, FinalQuizResult


NEXT_COURSE_MAP = {
    "interpolation_facile": "interpolation_moyen",
    "interpolation_moyen": "interpolation_difficile",
    "interpolation_difficile": None,
}


async def get_final_quiz(course_id: str) -> QuizPublic:
    db = get_database()
    quiz = await db.quizzes.find_one({"course_id": course_id, "quiz_type": "final"})
    if quiz is None:
        raise ValueError(f"Aucun quiz final trouvé pour le cours '{course_id}'")

    return QuizPublic(
        id=quiz["_id"],
        quiz_type=quiz["quiz_type"],
        module_id=quiz["module_id"],
        questions=[
            QuizQuestionPublic(question=q["question"], options=q["options"])
            for q in quiz["questions"]
        ],
    )


def _build_details(questions: list[dict], answers: list[int]) -> list[dict]:
    """Construit la correction détaillée, question par question."""
    details = []
    for q, given_answer in zip(questions, answers):
        correct_idx = q["correct"]
        is_correct = given_answer == correct_idx
        details.append({
            "question": q["question"],
            "options": q["options"],
            "given_index": given_answer,
            "correct_index": correct_idx,
            "correct": is_correct,
            "explanation": f"La bonne réponse est : « {q['options'][correct_idx]} ».",
        })
    return details


async def submit_final_quiz(
    course_id: str, student_id: str, answers: list[int]
) -> FinalQuizResult:
    db = get_database()
    quiz = await db.quizzes.find_one({"course_id": course_id, "quiz_type": "final"})
    if quiz is None:
        raise ValueError(f"Aucun quiz final trouvé pour le cours '{course_id}'")

    questions = quiz["questions"]
    if len(answers) != len(questions):
        raise ValueError("Le nombre de réponses ne correspond pas au nombre de questions")

    score = 0
    max_score = 0
    wrong_notions: list[str] = []

    for q, given_answer in zip(questions, answers):
        max_score += q["weight"]
        if given_answer == q["correct"]:
            score += q["weight"]
        else:
            wrong_notions.append(q["notion"])

    details = _build_details(questions, answers)
    module_id = quiz["module_id"]
    passed = score >= quiz["scoring"]["pass_threshold"]

    if passed:
        next_course_id = NEXT_COURSE_MAP.get(course_id)
        await db.student_progress.update_one(
            {"student_id": student_id},
            {
                "$set": {
                    f"modules.{module_id}.status": "completed" if next_course_id else "module_completed",
                    f"modules.{module_id}.current_course_id": next_course_id or course_id,
                    f"modules.{module_id}.final_quiz_score": score,
                    f"modules.{module_id}.lacune": None,
                }
            },
        )
        return FinalQuizResult(
            passed=True,
            score=score,
            max_score=max_score,
            next_course_id=next_course_id,
            retry_course_id=None,
            lacune=None,
            details=details,
        )
    else:
        lacune = max(set(wrong_notions), key=wrong_notions.count) if wrong_notions else None
        await db.student_progress.update_one(
            {"student_id": student_id},
            {
                "$set": {
                    f"modules.{module_id}.status": "failed_retry",
                    f"modules.{module_id}.final_quiz_score": score,
                    f"modules.{module_id}.lacune": lacune,
                }
            },
        )
        return FinalQuizResult(
            passed=False,
            score=score,
            max_score=max_score,
            next_course_id=None,
            retry_course_id=course_id,
            lacune=lacune,
            details=details,
        )
