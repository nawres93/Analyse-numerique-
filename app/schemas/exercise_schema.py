from pydantic import BaseModel


class ExercisePublic(BaseModel):
    """Vue envoyée à l'étudiant — SANS check_points complets (les réponses y).
    check_x expose uniquement les abscisses où l'étudiant doit répondre,
    ce qui ne fuite aucune réponse (juste "à quel x dois-je répondre").
    """
    id: str
    course_id: str
    type: str
    instructions: str
    given_points: list[list[float]]
    check_x: list[float]


class ExerciseSubmission(BaseModel):
    """Ce que l'étudiant envoie : les valeurs y qu'il propose, dans le même
    ordre que check_x reçu plus haut.
    Format : [y1, y2, ...]
    """
    submitted_points: list[list[float]]


class ExerciseResult(BaseModel):
    success: bool
    details: list[dict]
