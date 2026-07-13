"""
Routes réservées aux étudiants.
"""

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role
from app.models.user_model import UserRole
from app.schemas.user_schema import UserOut

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/dashboard", response_model=UserOut)
async def student_dashboard(current_user: dict = Depends(require_role(UserRole.STUDENT))):
    """
    Exemple de route protégée réservée aux students.
    Tu brancheras ici plus tard : accès aux modules d'apprentissage,
    historique des exercices sur les méthodes numériques, etc.
    """
    return UserOut.from_mongo(current_user)
