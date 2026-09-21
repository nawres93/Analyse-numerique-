from pydantic import BaseModel, EmailStr


class StudentResponse(BaseModel):

    id: str

    username: str

    email: EmailStr

    role: str

    status: str

    progress: int



class StudentCreate(BaseModel):

    full_name: str

    email: EmailStr

    password: str



class StudentUpdate(BaseModel):

    full_name: str | None = None

    email: EmailStr | None = None



class AdminDashboardResponse(BaseModel):

    total_students: int

    total_courses: int

    total_modules: int