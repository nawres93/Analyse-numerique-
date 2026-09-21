from pydantic import BaseModel, Field
from typing import Literal


class ExerciseModel(BaseModel):
    id: str = Field(alias="_id")
    course_id: str
    type: Literal["desmos"] = "desmos"
    instructions: str
    given_points: list[list[float]]     # points affichés à l'étudiant, ex: [[0,20],[10,35]]
    check_points: list[list[float]]     # [x, y_attendu] où on vérifie la réponse de l'étudiant
    tolerance: float = 0.5              # écart toléré sur y

    class Config:
        populate_by_name = True
