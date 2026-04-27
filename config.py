import os
import re
from dotenv import load_dotenv

load_dotenv()

_is_production = os.environ.get('FLASK_ENV') == 'production'


def _require_env(name: str) -> str:
    """Return an env-var or raise at startup (fail-fast)."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"FATAL: {name} is not set in the environment!")
    return value


class Config:
    # ── Secret key ──────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY and _is_production:
        raise RuntimeError("FATAL: SECRET_KEY not set in production environment!")
    SECRET_KEY = SECRET_KEY or 'dev-key-for-local-only'

    # ── Database ────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Session cookies ─────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = _is_production  # Only enforce HTTPS cookies in production
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = '__Host-session' if _is_production else 'session'

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = _is_production  # Only enforce HTTPS cookies in production
    REMEMBER_COOKIE_DURATION = 3600
    REMEMBER_COOKIE_SAMESITE = 'Lax'

    # CSRF tokens expire after 1 hour to limit replay window
    WTF_CSRF_TIME_LIMIT = 3600

    # Sessions are non-permanent by default (cleared on browser close)
    SESSION_PERMANENT = False

    # ── Password policy ─────────────────────────────────────────
    # Minimum length for user passwords (enforced in forms & model)
    PASSWORD_MIN_LENGTH = 8
    # Regex that the password must satisfy (upper, lower, digit, special)
    PASSWORD_COMPLEXITY_RE = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~])'
    )

    # ── Rate-limiter defaults ───────────────────────────────────
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_HEADERS_ENABLED = True   # Expose X-RateLimit-* headers

    # ── Max content length (reject huge uploads) ────────────────
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024   # 2 MB