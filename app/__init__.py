import os
from flask import Flask, render_template
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect  # NEW: Import CSRF protection
from config import Config
from app.extensions import db, migrate, login_manager

# Initialize CSRF protection object globally
csrf = CSRFProtect()

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
}

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    # 🛠️ THE FIX: Disable Talisman's strictness during development
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
        )

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)  # NEW: Activate CSRF protection

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    # ---- Security: Custom Error Handlers ----
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Prevent broken transactions from persisting
        return render_template('errors/500.html'), 500

    return app