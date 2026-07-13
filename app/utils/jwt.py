"""
Création et décodage des JSON Web Tokens (JWT).

Pourquoi deux tokens (access + refresh) et pas un seul ?
-----------------------------------------------------------
- L'ACCESS TOKEN a une durée de vie très courte (15 min ici). C'est celui
  qu'on envoie à CHAQUE requête protégée (Authorization: Bearer ...).
  S'il est volé, la fenêtre d'exploitation est petite.
- Le REFRESH TOKEN a une durée de vie longue (7 jours ici). Il sert
  UNIQUEMENT à demander un nouvel access token quand celui-ci expire,
  sans obliger l'utilisateur à retaper son mot de passe.
- On stocke les refresh tokens actifs en base (voir user_model.py) pour
  pouvoir les révoquer immédiatement (logout, changement de mot de passe,
  compte compromis) au lieu d'attendre qu'ils expirent naturellement.

"type" dans le payload permet de vérifier qu'un refresh token n'est pas
utilisé à la place d'un access token sur une route protégée (et inversement).
"""

import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def _create_token(subject: str, role: str, expires_delta: timedelta, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,           # user id
        "role": role,
        "type": token_type,       # "access" ou "refresh"
        "iat": now,
        "exp": now + expires_delta,
        "jti": str(uuid.uuid4()), # identifiant unique du token (utile pour le refresh)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str, role: str) -> str:
    return _create_token(
        subject=user_id,
        role=role,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(user_id: str, role: str) -> str:
    return _create_token(
        subject=user_id,
        role=role,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token(token: str) -> dict | None:
    """Retourne le payload décodé, ou None si le token est invalide/expiré."""
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


def generate_random_token() -> str:
    """Utilisé pour les tokens de vérification d'email et de reset password
    (pas des JWT, juste des chaînes aléatoires uniques stockées en base)."""
    return str(uuid.uuid4())
