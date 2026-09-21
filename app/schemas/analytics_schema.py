from pydantic import BaseModel
from typing import List


class EngagementPoint(BaseModel):
    month: str
    engagement: float


class UsagePoint(BaseModel):
    name: str
    value: float


class QuizInsights(BaseModel):
    average_grade: float
    completion_rate: float
    on_time_submissions: float


class AnalyticsResponse(BaseModel):
    engagement: List[EngagementPoint]
    usage: List[UsagePoint]
    insights: QuizInsights