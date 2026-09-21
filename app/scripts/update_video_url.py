import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


async def update_video():
    await connect_to_mongo()
    db = get_database()

    result = await db.courses.update_one(
        {"_id": "interpolation_facile"},
        {"$set": {"video_url": "http://localhost:8000/static/videos/interpolation_facile.mp4"}},
    )

    if result.modified_count == 1:
        print("video_url mis à jour pour interpolation_facile.")
    else:
        print("Aucune modification (le cours existe-t-il bien ?).")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(update_video())
