from datetime import datetime

from app.repositories.report_repository import ReportRepository


class ReportService:

    def __init__(self):
        self.repository = ReportRepository()

    async def get_reports(self):

        return {
            "reports": [
                {
                    "id": "monthly-performance",
                    "title": "Monthly performance summary",
                    "description": (
                        "PDF snapshot of student engagement, "
                        "grades and retention."
                    ),
                },
                {
                    "id": "module-publication",
                    "title": "Module publication report",
                    "description": (
                        "What was published, updated, "
                        "or scheduled this month."
                    ),
                },
                {
                    "id": "accreditation",
                    "title": "Export for accreditation",
                    "description": (
                        "CSV and PDF bundle for department "
                        "review and reporting."
                    ),
                },
            ]
        }

    async def monthly_performance(self):

        students = await self.repository.count_students()
        modules = await self.repository.count_modules()
        quizzes = await self.repository.count_quizzes()

        progress = await self.repository.get_progress()

        completed = 0

        for item in progress:

            if item.get("completed") is True:
                completed += 1

        if progress:
            completion_rate = (
                completed / len(progress)
            ) * 100
        else:
            completion_rate = 0

        return {
            "title": "Monthly performance summary",
            "generated_at": datetime.utcnow(),
            "students": students,
            "modules": modules,
            "quizzes": quizzes,
            "completion_rate": round(
                completion_rate,
                2
            ),
        }

    async def module_publication(self):

        modules = await self.repository.get_modules()

        published = 0
        draft = 0

        result = []

        for module in modules:

            status = module.get(
                "status",
                "Draft"
            )

            if status.lower() == "published":
                published += 1
            else:
                draft += 1

            result.append({
                "id": str(module.get("_id")),
                "title": module.get(
                    "title",
                    ""
                ),
                "code": module.get(
                    "code"
                ),
                "status": status,
            })

        return {
            "title": "Module publication report",
            "published": published,
            "draft": draft,
            "modules": result,
        }

    async def accreditation(self):

        students = await self.repository.count_students()
        courses = await self.repository.count_courses()
        modules = await self.repository.count_modules()
        quizzes = await self.repository.count_quizzes()

        return {
            "title": "Export for accreditation",
            "generated_at": datetime.utcnow(),
            "students": students,
            "courses": courses,
            "modules": modules,
            "quizzes": quizzes,
        }