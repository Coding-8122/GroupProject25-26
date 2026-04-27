from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions without the app instance
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """
    Loads the user object from the user ID stored in the session.
    Uses modern SQLAlchemy 2.0 syntax (db.session.get).
    """
    from app.models.user import User
    return db.session.get(User, int(user_id))