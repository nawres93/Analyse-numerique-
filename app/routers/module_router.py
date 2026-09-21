from fastapi import APIRouter

from app.services.module_service import ModuleService
from app.schemas.module_schema import ModuleUpdate


router = APIRouter(
    prefix="/modules",
    tags=["Modules"]
)

service = ModuleService()


# =========================
# GET MODULES
# =========================
@router.get("/")
async def get_modules(
    search: str | None = None
):
    return await service.get_modules(search)


# =========================
# UPDATE MODULE
# =========================
@router.put("/{module_id}")
async def update_module(
    module_id: str,
    data: ModuleUpdate
):
    return await service.update_module(
        module_id,
        data
    )


# =========================

# PUBLISH MODULE
# =========================
@router.put("/{module_id}/publish")
async def publish_module(
    module_id: str
):
    return await service.publish_module(module_id)