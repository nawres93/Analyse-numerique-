from fastapi import HTTPException

from app.repositories.quiz_repository import QuizRepository
from app.schemas.quiz_schema import QuizCreate, QuizUpdate


class QuizService:

    def __init__(self):
        self.repository = QuizRepository()


    async def get_quizzes(self, search: str | None = None):

        return await self.repository.get_all(search)


    async def get_quiz(self, quiz_id: str):

        quiz = await self.repository.get_by_id(quiz_id)

        if not quiz:
            raise HTTPException(
                status_code=404,
                detail="Quiz introuvable"
            )

        return quiz


    async def create_quiz(self, data: QuizCreate):

        quiz_data = {
            "title": data.title,
            "description": data.description,
            "questions": 0,
            "time": data.time,
            "attempts": 0,
            "status": data.status,
        }

        return await self.repository.create(quiz_data)


    async def update_quiz(
        self,
        quiz_id: str,
        data: QuizUpdate
    ):

        update_data = {
            key: value
            for key, value in data.model_dump().items()
            if value is not None
        }

        quiz = await self.repository.update(
            quiz_id,
            update_data
        )

        if not quiz:
            raise HTTPException(
                status_code=404,
                detail="Quiz introuvable"
            )

        return quiz


    async def delete_quiz(self, quiz_id: str):

        deleted = await self.repository.delete(quiz_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Quiz introuvable"
            )

        return {
            "message": "Quiz supprimé avec succès"
        }