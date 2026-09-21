from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class CourseVersion(BaseModel):
    id: str = Field(alias="_id")
    module_id: str
    level: Literal["facile", "moyen", "difficile"]
    title: str
    content_html: str
    video_url: str
    order: int

class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct: int          # index de la bonne réponse
    notion: str            # ex: "differences_divisees" -> sert à cibler la lacune
    weight: int = 1

class Quiz(BaseModel):
    id: str = Field(alias="_id")
    quiz_type: Literal["placement", "final"]
    module_id: str
    course_id: Optional[str] = None   # rempli seulement pour les quiz "final"
    questions: list[QuizQuestion]
    scoring: dict                      # {"faible_max": 4, "moyen_max": 7} pour placement
                                        # {"pass_threshold": 7} pour final

class Exercise(BaseModel):
    id: str = Field(alias="_id")
    course_id: str
    type: Literal["desmos"]
    instructions: str
    desmos_state: dict         # état attendu, exporté depuis Desmos

class ModuleProgress(BaseModel):
    level_detected: Optional[str] = None
    current_course_id: Optional[str] = None
    status: Literal["not_started", "in_progress", "completed", "failed_retry"] = "not_started"
    exercise_done: bool = False
    final_quiz_score: Optional[int] = None
    lacune: Optional[str] = None

class StudentProgress(BaseModel):
    id: str = Field(alias="_id")
    student_id: str
    modules: dict[str, ModuleProgress] = {}
    updated_at: datetime = Field(default_factory=datetime.utcnow)