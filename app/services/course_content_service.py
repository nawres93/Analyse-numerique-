from app.database.mongodb import get_database
from app.schemas.learning_course import CourseContentPublic


async def get_course_content(course_id: str) -> CourseContentPublic:
    db = get_database()
    course = await db.courses.find_one({"_id": course_id})
    if course is None:
        raise ValueError(f"Cours '{course_id}' introuvable")

    return CourseContentPublic(
        id=course["_id"],
        module_id=course["module_id"],
        level=course["level"],
        title=course["title"],
        content_html=course["content_html"],
        video_url=course["video_url"],
    )
