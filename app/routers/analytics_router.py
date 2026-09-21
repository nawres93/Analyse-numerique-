from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role
from app.models.user_model import UserRole
from app.services.analytics_service import AnalyticsService


router = APIRouter(
    prefix="/admin",
    tags=["Admin Analytics"]
)


@router.get("/analytics")
async def get_analytics(
    current_user: dict = Depends(
        require_role(UserRole.ADMIN)
    )
):
    service = AnalyticsService()

    return await service.get_analytics()