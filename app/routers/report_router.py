from fastapi import APIRouter, Depends

from app.services.report_service import ReportService

from app.schemas.report_schema import (
    ReportsResponse,
    MonthlyPerformanceReport,
    ModulePublicationReport,
    AccreditationReport,
)

from app.dependencies.auth import require_role
from app.models.user_model import UserRole


router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"]
)


@router.get(
    "",
    response_model=ReportsResponse
)
async def get_reports(
    current_user=Depends(
        require_role(UserRole.ADMIN)
    )
):
    service = ReportService()

    return await service.get_reports()


@router.get(
    "/monthly-performance",
    response_model=MonthlyPerformanceReport
)
async def monthly_performance(
    current_user=Depends(
        require_role(UserRole.ADMIN)
    )
):
    service = ReportService()

    return await service.monthly_performance()


@router.get(
    "/module-publication",
    response_model=ModulePublicationReport
)
async def module_publication(
    current_user=Depends(
        require_role(UserRole.ADMIN)
    )
):
    service = ReportService()

    return await service.module_publication()


@router.get(
    "/accreditation",
    response_model=AccreditationReport
)
async def accreditation(
    current_user=Depends(
        require_role(UserRole.ADMIN)
    )
):
    service = ReportService()

    return await service.accreditation()