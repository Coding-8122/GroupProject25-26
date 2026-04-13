from flask import Flask, render_template
from flask_talisman import Talisman
from config import Config
from app.extensions import db, migrate, login_manager

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

    Talisman(
        app,
        content_security_policy=_CSP,
        force_https=False,                     # Let reverse proxy handle TLS
        content_security_policy_nonce_in=['script-src'],
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    # ---- Security: Custom Error Handlers ----
    # Prevent Flask's default error pages from leaking stack traces,
    # file paths, or internal configuration to end users.
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Prevent broken transactions from persisting
        return render_template('errors/500.html'), 500

    return app