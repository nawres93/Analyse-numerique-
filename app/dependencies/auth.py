"""
Dépendances FastAPI : réutilisables dans n'importe quelle route via `Depends(...)`.

Comment ça marche concrètement ?
-----------------------------------
Sur une route protégée, tu écris :

    @router.get("/profile")
    async def profile(current_user: dict = Depends(get_current_user)):
        ...

FastAPI appelle automatiquement `get_current_user` AVANT ta fonction, lit le
header "Authorization: Bearer <token>", vérifie le JWT, et si tout est bon,
te donne directement l'utilisateur en base. Si le token est absent/invalide,
la requête est rejetée avec un 401 AVANT même d'entrer dans ta fonction.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user_model import UserRole
from app.repositories import user_repository as repo
from app.utils.jwt import decode_token

_bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> dict:
    token = credentials.credentials
    payload = decode_token(token)

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not payload or payload.get("type") != "access":
        raise unauthorized

    user = await repo.find_by_id(payload["sub"])
    if not user:
        raise unauthorized

    return user


def require_role(required_role: UserRole):
    """
    Fabrique une dépendance qui vérifie en plus que l'utilisateur a le bon rôle.

    Utilisation :
        @router.get("/admin/dashboard")
        async def dashboard(user: dict = Depends(require_role(UserRole.ADMIN))):
            ...
    """

    async def _check_role(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user["role"] != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé au rôle '{required_role.value}'.",
            )
        return current_user

    return _check_role
