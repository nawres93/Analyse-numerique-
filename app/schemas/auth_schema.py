"""
Schémas Pydantic liés à l'authentification.

Pourquoi Pydantic valide automatiquement ?
--------------------------------------------
Dès qu'une requête arrive sur une route qui attend un `RegisterRequest`,
FastAPI vérifie AVANT même d'exécuter ton code que :
- l'email est un email valide (grâce à EmailStr)
- le mot de passe respecte la longueur minimale
- tous les champs requis sont présents
Si ce n'est pas le cas, FastAPI renvoie automatiquement une erreur 422
avec le détail de ce qui ne va pas. Tu n'as pas besoin d'écrire ces
vérifications toi-même.
"""

from pydantic import BaseModel, EmailStr, Field

from app.models.user_model import UserRole


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Minimum 8 caractères. Idéalement mélange majuscules/minuscules/chiffres/symboles.",
    )
    role: UserRole = UserRole.STUDENT  # par défaut, un nouvel inscrit est student


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class VerifyEmailRequest(BaseModel):
    token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(
        ...,
        min_length=8,
        description="Minimum 8 caractères. Idéalement mélange majuscules/minuscules/chiffres/symboles.",
    )


class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class LogoutRequest(BaseModel):
    refresh_token: str
