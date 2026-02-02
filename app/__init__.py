from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager
from app.models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Set the login view for @login_required decorator
    login_manager.login_view = 'auth.login'

    # Register Blueprints (Controllers)
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app