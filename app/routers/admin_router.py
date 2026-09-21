from fastapi import APIRouter, Depends, Query, status

from app.services.admin_service import AdminService
from app.services.course_service import CourseService

from app.schemas.admin_schema import (
    AdminDashboardResponse,
    StudentResponse,
    StudentCreate,
    StudentUpdate
)

from app.schemas.course_schema import (
    CourseResponse,
    CourseCreate,
    CourseUpdate
)

from app.dependencies.auth import require_role
from app.models.user_model import UserRole



router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)



student_service = AdminService()
course_service = CourseService()



# ==========================
# Dashboard
# ==========================

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse
)
async def dashboard(
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await student_service.get_dashboard()



# =====================================================
# ====================== STUDENTS =====================
# =====================================================


# ==========================
# Get students + Search
# ==========================

@router.get(
    "/students",
    response_model=list[StudentResponse]
)
async def students(
    search: str | None = Query(
        default=None
    ),
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await student_service.get_students(
        search
    )



# ==========================
# Create student
# ==========================

@router.post(
    "/students",
    status_code=status.HTTP_201_CREATED
)
async def create_student(
    student: StudentCreate,
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    student_data = {

        "full_name": student.full_name,

        "email": student.email,

        "hashed_password": student.password,

        "role": UserRole.STUDENT.value,

        "is_verified": True,

        "refresh_tokens": []
    }


    student_id = await student_service.create_student(
        student_data
    )


    return {
        "message": "Student created",
        "id": student_id
    }



# ==========================
# Update student
# ==========================

@router.put(
    "/students/{student_id}"
)
async def update_student(
    student_id: str,
    student: StudentUpdate,
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    await student_service.update_student(
        student_id,
        student.model_dump(
            exclude_none=True
        )
    )


    return {
        "message": "Student updated"
    }



# ==========================
# Delete student
# ==========================

@router.delete(
    "/students/{student_id}"
)
async def delete_student(
    student_id: str,
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    await student_service.delete_student(
        student_id
    )


    return {
        "message": "Student deleted"
    }





# =====================================================
# ====================== COURSES ======================
# =====================================================



# ==========================
# Get courses + Search
# ==========================

@router.get(
    "/courses",
    response_model=list[CourseResponse]
)
async def get_courses(
    search: str | None = Query(
        default=None
    ),
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await course_service.get_courses(
        search
    )



# ==========================
# Create course
# ==========================

@router.post(
    "/courses",
    status_code=status.HTTP_201_CREATED,
    response_model=CourseResponse
)
async def create_course(
    course: CourseCreate,
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await course_service.create_course(
        course
    )



# ==========================
# Update course
# ==========================

@router.put(
    "/courses/{course_id}",
    response_model=CourseResponse
)
async def update_course(
    course_id: str,
    course: CourseUpdate,
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await course_service.update_course(
        course_id,
        course
    )



# ==========================
# Delete course
# ==========================

@router.delete(
    "/courses/{course_id}"
)
async def delete_course(
    course_id: str,
    user = Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await course_service.delete_course(
        course_id
    )