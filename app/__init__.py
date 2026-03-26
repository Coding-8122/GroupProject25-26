from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager

def create_app(config_class=Config):
    """
    Application factory pattern to create and configure the Flask app.
    This allows for multiple instances (e.g., development, testing, production).
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the newly created app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure Flask-Login redirects and message categories
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    return app