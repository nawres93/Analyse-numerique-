"""
Routes réservées aux administrateurs.

Toutes les routes ici sont protégées à la fois par :
1. get_current_user (il faut être connecté)
2. require_role(UserRole.ADMIN) (il faut être admin)
Ces deux dépendances font ça dans dependencies/auth.py.
"""

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role
from app.models.user_model import UserRole
from app.schemas.user_schema import UserOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=UserOut)
async def admin_dashboard(current_user: dict = Depends(require_role(UserRole.ADMIN))):
    """
    Exemple de route protégée réservée aux admins.
    Tu remplaceras ce contenu par tes vraies fonctionnalités admin plus tard
    (gestion des modules pédagogiques, statistiques d'utilisation, etc.).
    """
    return UserOut.from_mongo(current_user)
