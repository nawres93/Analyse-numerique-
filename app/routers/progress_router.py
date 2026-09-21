from fastapi import APIRouter, Depends

from app.schemas.progress_schema import (
    ProgressCreate,
    ProgressUpdate,
    ProgressResponse,
)

from app.services.progress_service import ProgressService


router = APIRouter(
    prefix="/admin/progress",
    tags=["Admin Progress"],
)


def get_progress_service():
    return ProgressService()


@router.get(
    "/",
    response_model=list[ProgressResponse],
)
async def get_progress(
    service: ProgressService = Depends(
        get_progress_service
    ),
):
    return await service.get_all_progress()


@router.get(
    "/student/{student_id}",
    response_model=list[ProgressResponse],
)
async def get_student_progress(
    student_id: str,
    service: ProgressService = Depends(
        get_progress_service
    ),
):
    return await service.get_student_progress(
        student_id
    )


@router.get(
    "/{progress_id}",
    response_model=ProgressResponse,
)
async def get_progress_by_id(
    progress_id: str,
    service: ProgressService = Depends(
        get_progress_service
    ),
):
    return await service.get_progress(
        progress_id
    )


@router.post(
    "/",
    response_model=ProgressResponse,
)
async def create_progress(
    data: ProgressCreate,
    service: ProgressService = Depends(
        get_progress_service
    ),
):
    return await service.create_progress(data)


@router.put(
    "/{progress_id}",
    response_model=ProgressResponse,
)
async def update_progress(
    progress_id: str,
    data: ProgressUpdate,
    service: ProgressService = Depends(
        get_progress_service
    ),
):
    return await service.update_progress(
        progress_id,
        data,
    )


@router.delete(
    "/{progress_id}",
)
async def delete_progress(
    progress_id: str,
    service: ProgressService = Depends(
        get_progress_service
    ),
):
    return await service.delete_progress(
        progress_id
    )