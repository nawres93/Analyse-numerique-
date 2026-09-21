from bson import ObjectId

from app.database.mongodb import get_database


class QuizRepository:

    async def get_all(self, search: str | None = None):

        db = get_database()

        query = {}

        if search:
            query = {
                "$or": [
                    {
                        "title": {
                            "$regex": search,
                            "$options": "i"
                        }
                    },
                    {
                        "description": {
                            "$regex": search,
                            "$options": "i"
                        }
                    }
                ]
            }

        quizzes = []

        cursor = db.quizzes.find(query)

        async for quiz in cursor:

            quizzes.append({
                "id": str(quiz["_id"]),
                "title": quiz.get("title", ""),
                "description": quiz.get("description", ""),
                "questions": quiz.get("questions", 0),
                "time": quiz.get("time", 0),
                "attempts": quiz.get("attempts", 0),
                "status": quiz.get("status", "Draft"),
            })

        return quizzes


    async def get_by_id(self, quiz_id: str):

        db = get_database()

        quiz = await db.quizzes.find_one({
            "_id": ObjectId(quiz_id)
        })

        if not quiz:
            return None

        return {
            "id": str(quiz["_id"]),
            "title": quiz.get("title", ""),
            "description": quiz.get("description", ""),
            "questions": quiz.get("questions", 0),
            "time": quiz.get("time", 0),
            "attempts": quiz.get("attempts", 0),
            "status": quiz.get("status", "Draft"),
        }


    async def create(self, data: dict):

        db = get_database()

        result = await db.quizzes.insert_one(data)

        return await self.get_by_id(str(result.inserted_id))


    async def update(self, quiz_id: str, data: dict):

        db = get_database()

        await db.quizzes.update_one(
            {
                "_id": ObjectId(quiz_id)
            },
            {
                "$set": data
            }
        )

        return await self.get_by_id(quiz_id)


    async def delete(self, quiz_id: str):

        db = get_database()

        result = await db.quizzes.delete_one({
            "_id": ObjectId(quiz_id)
        })

        return result.deleted_count > 0