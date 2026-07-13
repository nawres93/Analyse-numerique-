"""
Service d'authentification : toute la LOGIQUE MÉTIER vit ici.

Pourquoi une couche "service" séparée des routers ?
------------------------------------------------------
Le router ne fait QUE : recevoir la requête HTTP, appeler le service,
renvoyer la réponse HTTP. Toute la vraie logique (règles métier, appels
successifs à plusieurs repositories/utils) est ici. Ça permet par exemple
de tester cette logique sans avoir besoin de lancer un serveur HTTP.
"""

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.models.user_model import UserModel, UserRole
from app.repositories import user_repository as repo
from app.schemas.auth_schema import RegisterRequest
from app.utils.email import send_reset_password_email, send_verification_email
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_random_token,
)

RESET_TOKEN_VALIDITY = timedelta(minutes=30)


async def register_user(data: RegisterRequest) -> dict:
    existing = await repo.find_by_email(data.email)
    if existing:
        # Message volontairement générique : on ne confirme pas si l'email
        # existe déjà de façon trop précise pour éviter l'énumération de comptes,
        # mais ici un message clair est plus utile pédagogiquement pour toi.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte existe déjà avec cet email.",
        )

    verification_token = generate_random_token()
    hashed = hash_password(data.password)

    user_doc = UserModel.new_user_document(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hashed,
        role=data.role,
        verification_token=verification_token,
    )
    user_id = await repo.insert_user(user_doc)

    if settings.MAIL_USERNAME and settings.MAIL_SERVER:
        await send_verification_email(to=data.email, token=verification_token)
    else:
        # En mode développement sans SMTP, on marque l'utilisateur comme vérifié
        await repo.mark_email_verified(user_id)

    return {"id": user_id, "email": data.email, "role": data.role}


async def authenticate_user(email: str, password: str) -> dict:
    user = await repo.find_by_email(email)

    # Volontairement le même message d'erreur pour "email inconnu" et
    # "mot de passe incorrect" : ne jamais révéler si un email est enregistré.
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou mot de passe incorrect.",
    )

    if not user:
        raise invalid_credentials

    if not verify_password(password, user["hashed_password"]):
        raise invalid_credentials

    if not user["is_verified"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Merci de vérifier ton email avant de te connecter.",
        )

    user_id = str(user["_id"])
    access_token = create_access_token(user_id, user["role"])
    refresh_token = create_refresh_token(user_id, user["role"])

    await repo.add_refresh_token(user_id, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


async def refresh_access_token(refresh_token: str) -> dict:
    payload = decode_token(refresh_token)
    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token invalide ou expiré.",
    )

    if not payload or payload.get("type") != "refresh":
        raise invalid

    user_id = payload["sub"]

    # On vérifie que ce refresh token précis est toujours actif en base.
    # Ça permet de révoquer instantanément une session (logout) sans attendre
    # l'expiration naturelle du token.
    if not await repo.has_refresh_token(user_id, refresh_token):
        raise invalid

    user = await repo.find_by_id(user_id)
    if not user:
        raise invalid

    # Rotation du refresh token : on invalide l'ancien et on en émet un nouveau.
    # Ça limite les dégâts si un refresh token est volé (il ne reste utilisable
    # qu'une seule fois).
    await repo.remove_refresh_token(user_id, refresh_token)
    new_refresh_token = create_refresh_token(user_id, user["role"])
    await repo.add_refresh_token(user_id, new_refresh_token)

    new_access_token = create_access_token(user_id, user["role"])

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}


async def logout_user(refresh_token: str) -> None:
    payload = decode_token(refresh_token)
    if payload and payload.get("type") == "refresh":
        await repo.remove_refresh_token(payload["sub"], refresh_token)
    # Si le token est déjà invalide, on ne fait rien : le logout est "réussi"
    # dans tous les cas du point de vue de l'utilisateur.


async def verify_email(token: str) -> None:
    user = await repo.find_by_verification_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de vérification invalide.",
        )
    await repo.mark_email_verified(str(user["_id"]))


async def request_password_reset(email: str) -> None:
    user = await repo.find_by_email(email)
    if not user:
        # On ne révèle JAMAIS si l'email existe ou non : on répond toujours
        # comme si tout allait bien (même réponse HTTP côté router).
        return

    token = generate_random_token()
    expires_at = datetime.now(timezone.utc) + RESET_TOKEN_VALIDITY
    await repo.set_reset_token(str(user["_id"]), token, expires_at)
    await send_reset_password_email(to=email, token=token)


async def reset_password(token: str, new_password: str) -> None:
    user = await repo.find_by_reset_token(token)
    invalid = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token de réinitialisation invalide ou expiré.",
    )

    if not user:
        raise invalid

    expires_at = user.get("reset_password_token_expires")
    if not expires_at or datetime.now(timezone.utc) > expires_at.replace(tzinfo=timezone.utc):
        raise invalid

    hashed = hash_password(new_password)
    await repo.update_password(str(user["_id"]), hashed)
