from fastapi import HTTPException

from app.database.mongodb import get_database
from app.repositories.progress_repository import ProgressRepository
from app.schemas.progress import ModuleProgressPublic


# ---------------------------------------------------------------------------
# Fonction pour le CÔTÉ ÉTUDIANT (utilisée par app/routers/learning.py)
# ---------------------------------------------------------------------------
async def get_module_progress(student_id: str, module_id: str) -> ModuleProgressPublic:
    db = get_database()
    progress_doc = await db.student_progress.find_one({"student_id": student_id})

    if progress_doc is None or "modules" not in progress_doc or module_id not in progress_doc["modules"]:
        return ModuleProgressPublic()

    module_data = progress_doc["modules"][module_id]
    return ModuleProgressPublic(
        level_detected=module_data.get("level_detected"),
        current_course_id=module_data.get("current_course_id"),
        status=module_data.get("status", "not_started"),
        exercise_done=module_data.get("exercise_done", False),
        final_quiz_score=module_data.get("final_quiz_score"),
        lacune=module_data.get("lacune"),
    )


# ---------------------------------------------------------------------------
# Classe pour le CÔTÉ ADMIN (utilisée par app/routers/progress_router.py)
# — code original, récupéré tel quel —
# ---------------------------------------------------------------------------
class ProgressService:
    def __init__(self):
        self.repository = ProgressRepository()

    async def get_all_progress(self):
        return await self.repository.get_all()

    async def get_student_progress(self, student_id: str):
        return await self.repository.get_by_student(student_id)

    async def get_progress(self, progress_id: str):
        progress = await self.repository.get_by_id(progress_id)
        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")
        return progress

    async def create_progress(self, data):
        progress_data = data.model_dump(exclude_none=True)
        return await self.repository.create(progress_data)

    async def update_progress(self, progress_id: str, data):
        existing = await self.repository.get_by_id(progress_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Progress not found")
        update_data = data.model_dump(exclude_none=True)
        if not update_data:
            return existing
        return await self.repository.update(progress_id, update_data)

    async def delete_progress(self, progress_id: str):
        existing = await self.repository.get_by_id(progress_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Progress not found")
        deleted = await self.repository.delete(progress_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Progress not found")
        return {"message": "Progress deleted successfully", "id": progress_id}
