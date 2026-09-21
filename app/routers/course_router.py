from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modèle de données Pydantic pour valider les requêtes
class CourseUpdate(BaseModel):
    title: str
    code: str
    status: Optional[str] = "Published"

# Simulation d'une base de données locale
mock_courses = [
    {"id": 1, "title": "Analyse Numérique : Interpolation", "code": "NUM-01", "studentsCount": 120, "status": "Published"},
    {"id": 2, "title": "Résolution des Équations Non Linéaires", "code": "NUM-02", "studentsCount": 85, "status": "Draft"},
]

@app.get("/admin/courses")
async def get_courses(search: Optional[str] = None):
    if search:
        return [c for c in mock_courses if search.lower() in c["title"].lower() or search.lower() in c["code"].lower()]
    return mock_courses

@app.put("/admin/courses/{course_id}")
async def update_course(course_id: int, course_data: CourseUpdate):
    for course in mock_courses:
        if course["id"] == course_id:
            course["title"] = course_data.title
            course["code"] = course_data.code
            course["status"] = course_data.status
            return course
    raise HTTPException(status_code=404, detail="Cours non trouvé")
