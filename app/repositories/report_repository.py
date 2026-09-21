from app.database.mongodb import get_database


class ReportRepository:

    async def count_students(self):
        db = get_database()

        return await db.users.count_documents({
            "role": "student"
        })

    async def count_courses(self):
        db = get_database()

        return await db.courses.count_documents({})

    async def count_modules(self):
        db = get_database()

        return await db.modules.count_documents({})

    async def count_quizzes(self):
        db = get_database()

        return await db.quizzes.count_documents({})

    async def get_progress(self):
        db = get_database()

        return await db.progress.find({}).to_list(
            length=None
        )

    async def get_modules(self):
        db = get_database()

        return await db.modules.find({}).to_list(
            length=None
        )