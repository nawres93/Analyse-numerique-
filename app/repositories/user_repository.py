"""
Repository = la SEULE couche qui a le droit de parler directement à MongoDB.

Pourquoi cette séparation ?
-----------------------------
Si un jour tu changes de base de données (ex: passer de MongoDB à
PostgreSQL), tu ne modifies QUE ce fichier. Les services et routers, eux,
n'ont jamais connaissance de MongoDB directement : ils appellent juste
des fonctions comme `find_by_email(...)`.
"""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.database.mongodb import get_database


def _users_collection():
    return get_database()["users"]


async def find_by_email(email: str) -> dict | None:
    return await _users_collection().find_one({"email": email})


async def find_by_id(user_id: str) -> dict | None:
    if not ObjectId.is_valid(user_id):
        return None
    return await _users_collection().find_one({"_id": ObjectId(user_id)})


async def find_by_verification_token(token: str) -> dict | None:
    return await _users_collection().find_one({"verification_token": token})


async def find_by_reset_token(token: str) -> dict | None:
    return await _users_collection().find_one({"reset_password_token": token})


async def insert_user(user_document: dict) -> str:
    result = await _users_collection().insert_one(user_document)
    return str(result.inserted_id)


async def mark_email_verified(user_id: str) -> None:
    await _users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_verified": True, "verification_token": None,
                   "updated_at": datetime.now(timezone.utc)}},
    )


async def set_reset_token(user_id: str, token: str, expires_at: datetime) -> None:
    await _users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"reset_password_token": token,
                   "reset_password_token_expires": expires_at,
                   "updated_at": datetime.now(timezone.utc)}},
    )


async def update_password(user_id: str, hashed_password: str) -> None:
    await _users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"hashed_password": hashed_password,
                   "reset_password_token": None,
                   "reset_password_token_expires": None,
                   "refresh_tokens": [],  # on révoque toutes les sessions par sécurité
                   "updated_at": datetime.now(timezone.utc)}},
    )


async def add_refresh_token(user_id: str, refresh_token: str) -> None:
    await _users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"refresh_tokens": refresh_token}},
    )


async def remove_refresh_token(user_id: str, refresh_token: str) -> None:
    await _users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"refresh_tokens": refresh_token}},
    )


async def has_refresh_token(user_id: str, refresh_token: str) -> bool:
    user = await find_by_id(user_id)
    if not user:
        return False
    return refresh_token in user.get("refresh_tokens", [])

# =====================================================
# ADMIN - GESTION DES ETUDIANTS
# =====================================================


async def find_students(
    search: Optional[str] = None
) -> list[dict]:

    query = {
        "role": "student"
    }


    if search:

        query["$or"] = [
            {
                "full_name": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "email": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]


    cursor = _users_collection().find(query)


    students = []


    async for student in cursor:

        student["id"] = str(student["_id"])

        del student["_id"]

        students.append(student)


    return students



async def count_students() -> int:

    return await _users_collection().count_documents(
        {
            "role": "student"
        }
    )



async def create_student(
    student_document: dict
) -> str:

    result = await _users_collection().insert_one(
        student_document
    )

    return str(result.inserted_id)



async def update_student(
    student_id: str,
    data: dict
) -> bool:


    if not ObjectId.is_valid(student_id):
        return False


    result = await _users_collection().update_one(
        {
            "_id": ObjectId(student_id),
            "role": "student"
        },
        {
            "$set": {
                **data,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )


    return result.modified_count > 0



async def delete_student(
    student_id: str
) -> bool:


    if not ObjectId.is_valid(student_id):
        return False


    result = await _users_collection().delete_one(
        {
            "_id": ObjectId(student_id),
            "role": "student"
        }
    )


    return result.deleted_count > 0