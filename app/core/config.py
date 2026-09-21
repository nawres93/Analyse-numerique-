from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================
    # MongoDB
    # =========================
    MONGO_URI: str
    DB_NAME: str


    # =========================
    # JWT Authentication
    # =========================
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    # =========================
    # Email
    # =========================
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None

    MAIL_PORT: int = 587
    MAIL_SERVER: Optional[str] = None
    MAIL_FROM_NAME: Optional[str] = None


    # =========================
    # Google OAuth
    # =========================
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None


    # =========================
    # Facebook OAuth
    # =========================
    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_REDIRECT_URI: Optional[str] = None


    # =========================
    # Frontend
    # =========================
    FRONTEND_URL: str


    # =========================
    # CORS
    # =========================
    CORS_ORIGINS: str


    # =========================
    # Conversion CORS string -> list
    # =========================
    @property
    def cors_origins_list(self) -> list[str]:

        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


    # =========================
    # Load .env
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = Settings()