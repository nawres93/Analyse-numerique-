from datetime import datetime, timezone

from bson import ObjectId

from app.database.mongodb import get_database


class AdminRepository:

    def __init__(self):
        pass


    @property
    def collection(self):
        return get_database()["users"]


    async def count_students(self):

        return await self.collection.count_documents(
            {
                "role": "student"
            }
        )


    async def count_courses(self):

        db = get_database()

        return await db["courses"].count_documents({})


    async def count_modules(self):

        db = get_database()

        return await db["modules"].count_documents({})


    # ==========================
    # GET STUDENTS + SEARCH
    # ==========================

    async def get_students(self, search: str | None = None):

        query = {
            "role": "student"
        }


        if search:

            query["full_name"] = {
                "$regex": search,
                "$options": "i"
            }


        cursor = self.collection.find(query)


        students = []


        async for user in cursor:

            students.append(
                {
                    "id": str(user["_id"]),
                    "username": user.get("full_name"),
                    "email": user.get("email"),
                    "role": user.get("role"),
                    "status": 
                        "Active" if user.get("is_verified")
                        else "Inactive",
                    "progress": 0
                }
            )


        return students



    # ==========================
    # CREATE STUDENT
    # ==========================

    async def create_student(self, student: dict):

        result = await self.collection.insert_one(student)

        return str(result.inserted_id)



    # ==========================
    # UPDATE STUDENT
    # ==========================

    async def update_student(
            self,
            student_id: str,
            data: dict
    ):

        await self.collection.update_one(
            {
                "_id": ObjectId(student_id)
            },
            {
                "$set": {
                    **data,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )



    # ==========================
    # DELETE STUDENT
    # ==========================

    async def delete_student(
            self,
            student_id: str
    ):

        await self.collection.delete_one(
            {
                "_id": ObjectId(student_id)
            }
        )