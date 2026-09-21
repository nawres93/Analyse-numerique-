from app.repositories.admin_repository import AdminRepository


class AdminService:


    def __init__(self):

        self.repository = AdminRepository()



    async def get_dashboard(self):

        return {

            "total_students":
                await self.repository.count_students(),

            "total_courses":
                await self.repository.count_courses(),

            "total_modules":
                await self.repository.count_modules()
        }



    async def get_students(
            self,
            search: str | None = None
    ):

        return await self.repository.get_students(search)



    async def create_student(
            self,
            student_data: dict
    ):

        return await self.repository.create_student(
            student_data
        )



    async def update_student(
            self,
            student_id: str,
            data: dict
    ):

        return await self.repository.update_student(
            student_id,
            data
        )



    async def delete_student(
            self,
            student_id: str
    ):

        return await self.repository.delete_student(
            student_id
        )