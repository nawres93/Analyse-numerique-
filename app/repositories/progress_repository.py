from bson import ObjectId

from app.database.mongodb import get_database


class ProgressRepository:

    def __init__(self):
        self.collection_name = "progress"

    def _collection(self):
        db = get_database()
        return db[self.collection_name]

    def _serialize(self, document):
        if not document:
            return None

        return {
            "id": str(document["_id"]),
            "student_id": document.get("student_id"),
            "module_id": document.get("module_id"),
            "course_id": document.get("course_id"),
            "quiz_id": document.get("quiz_id"),
            "progress": document.get("progress", 0),
            "score": document.get("score"),
            "status": document.get("status", "In Progress"),
        }

    async def get_all(self):
        collection = self._collection()

        documents = await collection.find().to_list(length=None)

        return [
            self._serialize(document)
            for document in documents
        ]

    async def get_by_id(self, progress_id: str):

        if not ObjectId.is_valid(progress_id):
            return None

        collection = self._collection()

        document = await collection.find_one(
            {"_id": ObjectId(progress_id)}
        )

        return self._serialize(document)

    async def get_by_student(self, student_id: str):

        collection = self._collection()

        documents = await collection.find(
            {"student_id": student_id}
        ).to_list(length=None)

        return [
            self._serialize(document)
            for document in documents
        ]

    async def create(self, data: dict):

        collection = self._collection()

        result = await collection.insert_one(data)

        document = await collection.find_one(
            {"_id": result.inserted_id}
        )

        return self._serialize(document)

    async def update(
        self,
        progress_id: str,
        data: dict,
    ):

        if not ObjectId.is_valid(progress_id):
            return None

        collection = self._collection()

        await collection.update_one(
            {"_id": ObjectId(progress_id)},
            {"$set": data},
        )

        document = await collection.find_one(
            {"_id": ObjectId(progress_id)}
        )

        return self._serialize(document)

    async def delete(self, progress_id: str):

        if not ObjectId.is_valid(progress_id):
            return False

        collection = self._collection()

        result = await collection.delete_one(
            {"_id": ObjectId(progress_id)}
        )

        return result.deleted_count > 0