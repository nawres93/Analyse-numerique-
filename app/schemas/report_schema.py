from datetime import datetime
from typing import List

from pydantic import BaseModel


class ReportItem(BaseModel):
    id: str
    title: str
    description: str


class ReportsResponse(BaseModel):
    reports: List[ReportItem]


class MonthlyPerformanceReport(BaseModel):
    title: str
    generated_at: datetime
    students: int
    modules: int
    quizzes: int
    completion_rate: float


class ModuleReportItem(BaseModel):
    id: str
    title: str
    code: str | None = None
    status: str


class ModulePublicationReport(BaseModel):
    title: str
    published: int
    draft: int
    modules: List[ModuleReportItem]


class AccreditationReport(BaseModel):
    title: str
    generated_at: datetime
    students: int
    courses: int
    modules: int
    quizzes: int