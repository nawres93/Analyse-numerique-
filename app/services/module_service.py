from app.repositories.module_repository import ModuleRepository


class ModuleService:

    def __init__(self):
        self.repository = ModuleRepository()


    async def get_modules(self, search: str | None = None):
        return await self.repository.get_all(search)



    async def update_module(
        self,
        module_id: str,
        data
    ):
        return await self.repository.update(
            module_id,
            data.model_dump(exclude_unset=True)
        )



    async def publish_module(
        self,
        module_id: str
    ):
        return await self.repository.update(
            module_id,
            {
                "status": "Published"
            }
        )