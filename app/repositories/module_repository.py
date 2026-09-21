from app.database.mongodb import get_database
from bson import ObjectId


class ModuleRepository:

    async def get_all(self, search: str | None = None):

        db = get_database()

        query = {}

        if search:
            query = {
                "$or": [
                    {
                        "name": {
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

        modules = await db.modules.find(query).to_list(length=None)

        # MongoDB ObjectId -> String
        for module in modules:
            module["_id"] = str(module["_id"])

        return modules

    async def update(
        self,
        module_id: str,
        data: dict
    ):
        db = get_database()

        result = await db.modules.update_one(
            {
                "_id": ObjectId(module_id)
            },
            {
                "$set": data
            }
        )

        return {
            "message": "Module updated",
            "modified": result.modified_count
        }