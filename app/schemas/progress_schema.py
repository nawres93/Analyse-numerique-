from typing import Optional
from pydantic import BaseModel, Field


class ProgressCreate(BaseModel):
    student_id: str
    module_id: Optional[str] = None
    course_id: Optional[str] = None
    quiz_id: Optional[str] = None
    progress: float = Field(default=0, ge=0, le=100)
    score: Optional[float] = Field(default=None, ge=0, le=100)
    status: str = "In Progress"


class ProgressUpdate(BaseModel):
    progress: Optional[float] = Field(default=None, ge=0, le=100)
    score: Optional[float] = Field(default=None, ge=0, le=100)
    status: Optional[str] = None


class ProgressResponse(BaseModel):
    id: str
    student_id: str
    module_id: Optional[str] = None
    course_id: Optional[str] = None
    quiz_id: Optional[str] = None
    progress: float
    score: Optional[float] = None
    status: str