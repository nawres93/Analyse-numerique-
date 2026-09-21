from pydantic import BaseModel
from typing import Optional


class ModuleProgressPublic(BaseModel):
    level_detected: Optional[str] = None
    current_course_id: Optional[str] = None
    status: str = "not_started"   # not_started | in_progress | completed | failed_retry | module_completed
    exercise_done: bool = False
    final_quiz_score: Optional[int] = None
    lacune: Optional[str] = None
    

    