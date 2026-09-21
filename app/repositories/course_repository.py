from bson import ObjectId
from app.database.mongodb import get_database


class CourseRepository:

    def __init__(self):
        self.collection_name = "courses"


    def collection(self):
        db = get_database()
        return db[self.collection_name]


    # ==========================
    # GET ALL COURSES
    # ==========================
    async def get_courses(self, search: str | None = None):

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
                        "code": {
                            "$regex": search,
                            "$options": "i"
                        }
                    }
                ]
            }


        courses = []

        cursor = self.collection().find(query)

        async for course in cursor:

            courses.append(
                {
                    "id": str(course["_id"]),
                    "title": course.get("title"),
                    "code": course.get("code"),
                    "description": course.get("description"),
                    "status": course.get("status", "Draft")
                }
            )


        return courses



    # ==========================
    # GET COURSE BY ID
    # ==========================
    async def get_course_by_id(self, course_id: str):

        if not ObjectId.is_valid(course_id):
            return None


        course = await self.collection().find_one(
            {
                "_id": ObjectId(course_id)
            }
        )


        if course:

            return {
                "id": str(course["_id"]),
                "title": course.get("title"),
                "code": course.get("code"),
                "description": course.get("description"),
                "status": course.get("status", "Draft")
            }


        return None



    # ==========================
    # CREATE COURSE
    # ==========================
    async def create_course(self, course_data: dict):

        result = await self.collection().insert_one(
            course_data
        )


        new_course = await self.get_course_by_id(
            str(result.inserted_id)
        )


        return new_course



    # ==========================
    # UPDATE COURSE
    # ==========================
    async def update_course(
        self,
        course_id: str,
        course_data: dict
    ):

        if not ObjectId.is_valid(course_id):
            return None


        await self.collection().update_one(
            {
                "_id": ObjectId(course_id)
            },
            {
                "$set": course_data
            }
        )


        return await self.get_course_by_id(course_id)



    # ==========================
    # DELETE COURSE
    # ==========================
    async def delete_course(
        self,
        course_id: str
    ):

        if not ObjectId.is_valid(course_id):
            return False


        result = await self.collection().delete_one(
            {
                "_id": ObjectId(course_id)
            }
        )


        return result.deleted_count > 0