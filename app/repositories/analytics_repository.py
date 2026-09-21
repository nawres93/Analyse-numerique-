from app.database.mongodb import get_database


class AnalyticsRepository:

    async def get_monthly_engagement(self):

        db = get_database()

        total_students = await db.users.count_documents({
            "role": "etudiant"
        })

        return {
            "total_students": total_students
        }

    async def get_usage(self):

        db = get_database()

        total_courses = await db.courses.count_documents({})

        total_modules = await db.modules.count_documents({})

        total_quizzes = await db.quizzes.count_documents({})

        return {
            "total_courses": total_courses,
            "total_modules": total_modules,
            "total_quizzes": total_quizzes
        }

    async def get_quiz_statistics(self):

        db = get_database()

        total_quizzes = await db.quizzes.count_documents({})

        return {
            "total_quizzes": total_quizzes
        }