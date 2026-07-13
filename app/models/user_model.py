"""
Modèle User : représente la structure d'un document dans la collection "users".

Pourquoi séparer models/ et schemas/ ?
----------------------------------------
- models/  -> la forme des données TELLE QU'ELLE EST STOCKÉE en base
  (inclut le mot de passe hashé, les champs internes comme is_verified,
  refresh_token, etc.)
- schemas/ -> la forme des données envoyées/reçues par l'API
  (ex: on ne renvoie JAMAIS le mot de passe hashé au frontend !)

Si on utilisait un seul et même modèle partout, on risquerait un jour de
renvoyer accidentellement le hash du mot de passe dans une réponse API.
Séparer les deux rend cette erreur beaucoup plus difficile à commettre.
"""

from datetime import datetime, timezone
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"


class UserModel:
    """
    Représente un utilisateur tel que stocké dans MongoDB.
    Ce n'est pas un modèle Pydantic strict : MongoDB stocke des dicts,
    donc on utilise cette classe surtout comme référence documentée
    de la structure d'un document "users".

    Structure d'un document :
    {
        "_id": ObjectId,
        "full_name": str,
        "email": str (unique),
        "hashed_password": str,
        "role": "admin" | "student",
        "is_verified": bool,
        "verification_token": str | None,
        "reset_password_token": str | None,
        "reset_password_token_expires": datetime | None,
        "refresh_tokens": list[str],   # tokens de refresh actifs (multi-appareils)
        "created_at": datetime,
        "updated_at": datetime,
    }
    """

    @staticmethod
    def new_user_document(full_name: str, email: str, hashed_password: str,
                           role: UserRole, verification_token: str) -> dict:
        now = datetime.now(timezone.utc)
        return {
            "full_name": full_name,
            "email": email,
            "hashed_password": hashed_password,
            "role": role.value,
            "is_verified": False,
            "verification_token": verification_token,
            "reset_password_token": None,
            "reset_password_token_expires": None,
            "refresh_tokens": [],
            "created_at": now,
            "updated_at": now,
        }
