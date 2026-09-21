from pydantic import BaseModel


class QuizQuestionPublic(BaseModel):
    """Version envoyée au frontend — sans la bonne réponse."""
    question: str
    options: list[str]
    # ⚠️ pas de champ `correct` ici, volontairement


class QuizPublic(BaseModel):
    id: str
    quiz_type: str
    module_id: str
    questions: list[QuizQuestionPublic]


class QuizSubmission(BaseModel):
    """Ce que le frontend envoie : l'index choisi pour chaque question, dans l'ordre."""
    answers: list[int]


class PlacementResult(BaseModel):
    score: int
    max_score: int
    level_detected: str
    course_id: str


# --- À AJOUTER à la fin de ton fichier app/schemas/quiz.py existant ---
# (ne remplace pas le fichier, ajoute juste cette classe en plus)

class FinalQuizResult(BaseModel):
    passed: bool
    score: int
    max_score: int
    next_course_id: str | None
    retry_course_id: str | None
    lacune: str | None
    details: list[dict]

