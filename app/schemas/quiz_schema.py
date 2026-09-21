from pydantic import BaseModel, Field
from typing import Optional


class QuizCreate(BaseModel):
    title: str
    description: str
    time: int = Field(gt=0)
    status: str = "Draft"


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time: Optional[int] = Field(default=None, gt=0)
    status: Optional[str] = None


class QuizResponse(BaseModel):
    id: str
    title: str
    description: str
    questions: int
    time: int
    attempts: int
    status: str