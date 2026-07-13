"""
Point d'entrée de l'application FastAPI.

Ce fichier reste volontairement TRÈS court : il ne fait qu'assembler les
morceaux (config, base de données, routers). Toute la logique vit ailleurs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.mongodb import close_mongo_connection, connect_to_mongo
from app.routers import admin_router, auth_router, student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Exécuté UNE fois au démarrage du serveur.
    await connect_to_mongo()
    yield
    # Exécuté UNE fois à l'arrêt du serveur.
    await close_mongo_connection()


app = FastAPI(
    title="Numerical Analysis Platform API",
    description="Backend d'authentification sécurisée pour la plateforme pédagogique de numerical analysis.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(student_router.router)


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "API is running"}
