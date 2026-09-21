from fastapi import APIRouter, Depends, Query

from app.schemas.quiz_schema import (
    QuizCreate,
    QuizUpdate,
)
from app.services.quiz_service import QuizService


router = APIRouter(
    prefix="/quizzes",
    tags=["Admin - Quizzes"]
)


def get_service():
    return QuizService()


@router.get("/")
async def get_quizzes(
    search: str | None = Query(default=None),
    service: QuizService = Depends(get_service),
):
    return await service.get_quizzes(search)


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    service: QuizService = Depends(get_service),
):
    return await service.get_quiz(quiz_id)


@router.post("/")
async def create_quiz(
    data: QuizCreate,
    service: QuizService = Depends(get_service),
):
    return await service.create_quiz(data)


@router.put("/{quiz_id}")
async def update_quiz(
    quiz_id: str,
    data: QuizUpdate,
    service: QuizService = Depends(get_service),
):
    return await service.update_quiz(
        quiz_id,
        data
    )


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    service: QuizService = Depends(get_service),
):
    return await service.delete_quiz(quiz_id)