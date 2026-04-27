import logging
import os
from flask import Flask, render_template, request
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from app.extensions import db, migrate, login_manager

# Initialize security extensions globally to prevent circular imports
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "60 per hour"],
    storage_uri="memory://",
)

# Content Security Policy (CSP) for Production
_CSP = {
    'default-src': "'self'",
    'script-src': ["'self'", 'https://cdn.jsdelivr.net'],
    'style-src': ["'self'", 'https://cdn.jsdelivr.net', "'unsafe-inline'"],
    'img-src': ["'self'", 'data:'],
    'font-src': ["'self'", 'https://cdn.jsdelivr.net'],
    'object-src': "'none'",
}

# Security Event Logger configuration
security_log = logging.getLogger('security')
security_log.setLevel(logging.INFO)
if not security_log.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('%(asctime)s SECURITY %(levelname)s: %(message)s'))
    security_log.addHandler(_handler)

def create_app(config_class=Config, test_config=None):
    """Application factory for RecoveryTracker."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    # 1. Initialize Core Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # 2. Security Hardening (Talisman)
    is_prod = os.environ.get('FLASK_ENV') == 'production'
    if is_prod and not app.config.get('TESTING'):
        Talisman(app, content_security_policy=_CSP, force_https=True, session_cookie_secure=True)
    else:
        Talisman(app, content_security_policy=None, force_https=False)

    # 3. Register Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.main import main_bp
    app.register_blueprint(main_bp)
    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    # 4. Defensive HTTP Headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        if hasattr(request, 'endpoint') and request.endpoint and not request.endpoint.startswith('static'):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response

    return app