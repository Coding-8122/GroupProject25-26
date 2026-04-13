import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY and os.environ.get('FLASK_ENV') == 'production':
        raise RuntimeError("FATAL: SECRET_KEY not set in production environment!")
    SECRET_KEY = SECRET_KEY or 'dev-key-for-local-only'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_DURATION = 3600

    # CSRF tokens expire after 1 hour to limit replay window
    WTF_CSRF_TIME_LIMIT = 3600

    # Sessions are non-permanent by default (cleared on browser close)
    SESSION_PERMANENT = False