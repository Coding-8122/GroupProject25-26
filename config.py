import os
from dotenv import load_dotenv

load_dotenv()
_is_prod = os.environ.get("FLASK_ENV") == "production"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY and _is_prod:
        raise RuntimeError("FATAL: SECRET_KEY not set in production!")
    SECRET_KEY = SECRET_KEY or "dev-key-for-local-only"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = _is_prod
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = _is_prod

    # Rate Limiting & Uploads
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
