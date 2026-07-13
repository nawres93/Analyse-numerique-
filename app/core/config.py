"""
Configuration centrale de l'application.

Pourquoi ce fichier existe ?
----------------------------
Toutes les valeurs qui changent selon l'environnement (dev, test, production)
ne doivent JAMAIS être écrites en dur dans le code (ex: mot de passe MongoDB,
clé secrète JWT). On les met dans un fichier .env, et Pydantic les charge
ici de façon typée et validée. Si une variable manque, l'application refuse
de démarrer au lieu de planter plus tard en pleine requête utilisateur.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MongoDB
    MONGO_URI: str
    DB_NAME: str = "numerical_analysis_platform"

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = "Numerical Analysis Platform"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # CORS (liste séparée par des virgules dans le .env)
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Instance unique, importée partout ailleurs dans le projet.
# On ne veut PAS recharger le .env à chaque fois qu'on a besoin d'une valeur.
settings = Settings()
