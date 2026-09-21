from typing import Optional
from pydantic import BaseModel


class CourseCreate(BaseModel):
    """Payload envoyé par l'admin pour créer un cours."""
    module_id: str
    level: str          # "facile" | "moyen" | "difficile"
    title: str
    content_html: str
    video_url: str = ""
    order: int = 0


class CourseUpdate(BaseModel):
    """Payload envoyé par l'admin pour modifier un cours existant.
    Tous les champs sont optionnels : on ne modifie que ce qui est fourni.
    """
    module_id: Optional[str] = None
    level: Optional[str] = None
    title: Optional[str] = None
    content_html: Optional[str] = None
    video_url: Optional[str] = None
    order: Optional[int] = None


class CoursePublic(BaseModel):
    """Vue renvoyée par l'API."""
    id: str
    module_id: str
    level: str
    title: str
    content_html: str
    video_url: str
    order: int = 0


# admin_router.py importe ce nom précis (CourseResponse) — on le fait pointer
# vers la même classe que CoursePublic pour ne pas dupliquer la définition.
# Si les deux ont vraiment besoin de champs différents plus tard, on les
# séparera en deux vraies classes distinctes.
CourseResponse = CoursePublic
