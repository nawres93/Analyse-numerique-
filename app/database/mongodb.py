from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


client = AsyncIOMotorClient(
    settings.MONGO_URI
)


database = None


async def connect_to_mongo():

    global database

    database = client[settings.DB_NAME]

    try:
        await client.admin.command("ping")
        print("✓ MongoDB connecté avec succès")

    except Exception as e:
        print("Erreur MongoDB :", e)



async def close_mongo_connection():

    client.close()
    print("MongoDB fermé")



def get_database():

    if database is None:
        raise RuntimeError(
            "MongoDB n'est pas connecté"
        )

    return database
    