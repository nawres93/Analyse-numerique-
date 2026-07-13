"""
Schéma de sortie pour un utilisateur.

Règle de sécurité essentielle :
--------------------------------
UserOut ne contient JAMAIS le hashed_password, ni les tokens de reset/verify.
C'est le seul schéma qu'on doit utiliser pour renvoyer un utilisateur au
frontend (ex: GET /auth/me).
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.user_model import UserRole


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: UserRole
    is_verified: bool
    created_at: datetime

    @staticmethod
    def from_mongo(document: dict) -> "UserOut":
        return UserOut(
            id=str(document["_id"]),
            full_name=document["full_name"],
            email=document["email"],
            role=document["role"],
            is_verified=document["is_verified"],
            created_at=document["created_at"],
        )
