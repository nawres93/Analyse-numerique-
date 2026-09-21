from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from fastapi.staticfiles import StaticFiles
from app.database.mongodb import (
    close_mongo_connection,
    connect_to_mongo,
)

from app.routers import (
    admin_router,
    auth_router,
    learning,
    progress_router,
    report_router,
    student_router,
    module_router,
    quiz_router,
)

from app.routers.analytics_router import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Connexion MongoDB
    await connect_to_mongo()

    yield

    # Fermeture MongoDB
    await close_mongo_connection()


app = FastAPI(
    title="Numerical Analysis Platform API",
    description="Backend de la plateforme pédagogique de Numerical Analysis.",
    version="1.0.0",
    lifespan=lifespan,
)

# =========================
# FICHIERS STATIQUES (vidéos, etc.)
# =========================

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTERS
# =========================

app.include_router(auth_router.router)

app.include_router(admin_router.router)

app.include_router(student_router.router)

app.include_router(progress_router.router)

app.include_router(analytics_router)

app.include_router(report_router.router)

app.include_router(learning.router)

# =========================
# MODULES
# =========================

app.include_router(
    module_router.router,
    prefix="/admin",
)


# =========================
# QUIZZES
# =========================

app.include_router(
    quiz_router.router,
    prefix="/admin",
)


# =========================
# HEALTH CHECK
# =========================

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "message": "API is running",
    }