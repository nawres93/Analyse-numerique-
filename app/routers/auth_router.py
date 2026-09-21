"""
Routes d'authentification.

Rappel du rôle d'un router : recevoir la requête, appeler le service,
renvoyer la réponse. Pas de logique métier ici.
"""

from fastapi import APIRouter, Depends, status
from fastapi import Request
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.utils.google_oauth import build_google_auth_url


from app.dependencies.auth import get_current_user
from app.schemas.auth_schema import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    VerifyEmailRequest,
)
from app.schemas.user_schema import UserOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    result = await auth_service.register_user(data)
    return {
        "message": "Compte créé. Vérifie ta boîte mail pour activer ton compte.",
        "user": result,
    }


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    tokens = await auth_service.authenticate_user(data.email, data.password)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest):
    tokens = await auth_service.refresh_access_token(data.refresh_token)
    return tokens


@router.post("/logout")
async def logout(data: LogoutRequest):
    await auth_service.logout_user(data.refresh_token)
    return {"message": "Déconnexion réussie."}


@router.post("/verify-email")
async def verify_email(data: VerifyEmailRequest):
    await auth_service.verify_email(data.token)
    return {"message": "Email vérifié avec succès. Tu peux te connecter."}


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    await auth_service.request_password_reset(data.email)
    # Réponse volontairement identique que l'email existe ou non.
    return {"message": "Si un compte existe avec cet email, un lien de réinitialisation a été envoyé."}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    await auth_service.reset_password(data.token, data.new_password)
    return {"message": "Mot de passe réinitialisé avec succès."}


@router.get("/me", response_model=UserOut)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserOut.from_mongo(current_user)


@router.get("/google")
async def google_login():
    return RedirectResponse(build_google_auth_url())


@router.get("/google/callback")
async def google_callback(code: str):
    tokens = await auth_service.authenticate_google_user(code)
    redirect_url = (
        f"{settings.FRONTEND_URL}/auth/google/success"
        f"?access_token={tokens['access_token']}"
        f"&refresh_token={tokens['refresh_token']}"
    )
    return RedirectResponse(redirect_url)
