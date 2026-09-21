from fastapi import HTTPException, status

from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import CourseCreate, CourseUpdate,CoursePublic
from app.database.mongodb import get_database


class CourseService:

    def __init__(self):
        self.repository = CourseRepository()


    async def get_courses(self, search=None):
        return await self.repository.get_courses(search)


    async def create_course(self, course: CourseCreate):
        return await self.repository.create_course(
            course.model_dump()
        )


    async def update_course(
        self,
        course_id: str,
        course: CourseUpdate
    ):

        data = {
            k: v
            for k, v in course.model_dump().items()
            if v is not None
        }

        return await self.repository.update_course(
            course_id,
            data
        )


    async def delete_course(self, course_id: str):

        result = await self.repository.delete_course(
            course_id
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        return {
            "message": "Course deleted successfully"
        }




async def get_course(course_id: str) -> CoursePublic:
    db = get_database()
    course = await db.courses.find_one({"_id": course_id})
    if course is None:
        raise ValueError(f"Cours '{course_id}' introuvable")

    return CoursePublic(
        id=course["_id"],
        module_id=course["module_id"],
        level=course["level"],
        title=course["title"],
        content_html=course["content_html"],
        video_url=course["video_url"],
    )
