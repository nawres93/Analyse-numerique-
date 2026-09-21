import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


VIDEO_UPDATES = {
    "interpolation_moyen": "http://localhost:8000/static/videos/interpolation_moyen.mp4",
    "interpolation_difficile": "http://localhost:8000/static/videos/interpolation_difficile.mp4",
}


async def update_videos():
    await connect_to_mongo()
    db = get_database()

    for course_id, url in VIDEO_UPDATES.items():
        result = await db.courses.update_one(
            {"_id": course_id},
            {"$set": {"video_url": url}},
        )
        if result.modified_count == 1:
            print(f"video_url mis à jour pour {course_id}.")
        else:
            print(f"Aucune modification pour {course_id} (déjà à jour, ou cours introuvable).")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(update_videos())