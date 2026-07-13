"""
Connexion à MongoDB via Motor.

Pourquoi Motor et pas pymongo directement ?
--------------------------------------------
FastAPI est asynchrone (async def). Si on utilisait pymongo (synchrone),
chaque requête à la base de données bloquerait tout le serveur pendant son
exécution -> plus aucune autre requête ne pourrait être traitée en même temps.
Motor est la version asynchrone officielle de pymongo, compatible avec
async/await, et donc avec les performances de FastAPI.

On ouvre UNE seule connexion (un "client") au démarrage de l'app, et on la
réutilise partout. On ne crée jamais une connexion par requête.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongodb = MongoDB()


async def connect_to_mongo() -> None:
    """Appelé au démarrage de FastAPI (startup event)."""
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
        mongodb.database = mongodb.client[settings.DB_NAME]

        # Index unique sur l'email : empêche deux comptes avec le même email,
        # même en cas de "race condition" (deux requêtes register simultanées).
        await mongodb.database["users"].create_index("email", unique=True)
        print("✓ MongoDB connecté avec succès")
    except Exception as e:
        print(f"⚠️  AVERTISSEMENT: Impossible de se connecter à MongoDB ({e})")
        print(f"   L'API démarre en mode développement sans base de données.")
        print(f"   Les endpoints d'authentification ne fonctionneront pas.")
        print(f"   Pour utiliser MongoDB: installez-le ou configurez MONGO_URI dans .env")
        mongodb.client = None
        mongodb.database = None


async def close_mongo_connection() -> None:
    """Appelé à l'arrêt de FastAPI (shutdown event). Libère proprement la connexion."""
    if mongodb.client:
        mongodb.client.close()


def get_database() -> AsyncIOMotorDatabase:
    """Utilisé par les repositories pour accéder aux collections."""
    return mongodb.database
