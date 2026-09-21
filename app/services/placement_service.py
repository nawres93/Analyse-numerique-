from app.database.mongodb import get_database
from app.schemas.quiz import QuizPublic, QuizQuestionPublic, PlacementResult


async def get_placement_quiz(module_id: str) -> QuizPublic:
    db = get_database()
    quiz = await db.quizzes.find_one({"module_id": module_id, "quiz_type": "placement"})
    if quiz is None:
        raise ValueError(f"Aucun quiz de placement trouvé pour le module '{module_id}'")

    return QuizPublic(
        id=quiz["_id"],
        quiz_type=quiz["quiz_type"],
        module_id=quiz["module_id"],
        questions=[
            QuizQuestionPublic(question=q["question"], options=q["options"])
            for q in quiz["questions"]
        ],
    )


def determine_level(score: int, scoring: dict) -> str:
    if score <= scoring["faible_max"]:
        return "faible"
    elif score <= scoring["moyen_max"]:
        return "moyen"
    return "fort"


LEVEL_TO_COURSE_SUFFIX = {
    "faible": "facile",
    "moyen": "moyen",
    "fort": "difficile",
}


async def submit_placement_quiz(
    module_id: str, student_id: str, answers: list[int]
) -> PlacementResult:
    db = get_database()
    quiz = await db.quizzes.find_one({"module_id": module_id, "quiz_type": "placement"})
    if quiz is None:
        raise ValueError(f"Aucun quiz de placement trouvé pour le module '{module_id}'")

    questions = quiz["questions"]
    if len(answers) != len(questions):
        raise ValueError("Le nombre de réponses ne correspond pas au nombre de questions")

    score = 0
    max_score = 0
    for q, given_answer in zip(questions, answers):
        max_score += q["weight"]
        if given_answer == q["correct"]:
            score += q["weight"]

    level = determine_level(score, quiz["scoring"])
    course_id = f"{module_id}_{LEVEL_TO_COURSE_SUFFIX[level]}"

    # Mise à jour de student_progress
    await db.student_progress.update_one(
        {"student_id": student_id},
        {
            "$set": {
                f"modules.{module_id}.level_detected": level,
                f"modules.{module_id}.current_course_id": course_id,
                f"modules.{module_id}.status": "in_progress",
            }
        },
        upsert=True,
    )

    return PlacementResult(
        score=score, max_score=max_score, level_detected=level, course_id=course_id
    )