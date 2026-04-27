import logging
import os
from flask import Flask, render_template, request
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from app.extensions import db, migrate, login_manager

# Initialize CSRF protection object globally
csrf = CSRFProtect()

# Initialize rate limiter globally
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "60 per hour"],
    storage_uri="memory://",
)

_is_production = os.environ.get('FLASK_ENV') == 'production'

# Content Security Policy — whitelists only the CDNs this app actually uses
_CSP = {
    'default-src': '\'self\'',
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        '\'unsafe-inline\'',   # Required by Bootstrap
    ],
    'img-src': '\'self\' data:',
    'font-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
    ],
    'object-src': '\'none\'',
    'base-uri': '\'self\'',
    'form-action': '\'self\'',
    'frame-ancestors': '\'none\'',
    'upgrade-insecure-requests': '',
}

# ── Security-event logger ──────────────────────────────────────
security_log = logging.getLogger('security')
security_log.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(
    '%(asctime)s  SECURITY  %(levelname)s  %(message)s'
))
security_log.addHandler(_handler)


def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    # ── Talisman (HTTP security headers) ──
    if os.environ.get('FLASK_ENV') == 'development' or not _is_production:
        Talisman(app, content_security_policy=None, force_https=False)
    else:
        Talisman(
            app,
            content_security_policy=_CSP,
            force_https=True,
            content_security_policy_nonce_in=['script-src'],
            session_cookie_secure=True,
            strict_transport_security=True,
            strict_transport_security_max_age=31536000,
            strict_transport_security_include_subdomains=True,
            referrer_policy='strict-origin-when-cross-origin',
            permissions_policy={
                'geolocation': '()',
                'microphone': '()',
                'camera': '()',
            },
        )

    # ── Initialize Extensions ──
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    # Force re-authentication for sensitive operations
    login_manager.refresh_view = 'auth.login'
    login_manager.needs_refresh_message = 'Please re-authenticate to access this page.'
    login_manager.needs_refresh_message_category = 'warning'
    # Harden session protection against session fixation
    login_manager.session_protection = 'strong'

    # ── Register Blueprints ──
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    # ── After-request: defensive headers ──
    @app.after_request
    def set_security_headers(response):
        # Prevent browsers from MIME-sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Don't leak the server stack to attackers
        response.headers.pop('Server', None)
        # Prevent caching of authenticated pages
        if hasattr(request, 'endpoint') and request.endpoint and \
                not request.endpoint.startswith('static'):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
        return response

    # ── Security: Custom Error Handlers ──
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(429)
    def ratelimit_error(error):
        security_log.warning(
            'Rate limit exceeded: ip=%s path=%s',
            request.remote_addr, request.path,
        )
        return render_template('errors/429.html'), 429

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Prevent broken transactions from persisting
        return render_template('errors/500.html'), 500

    return app