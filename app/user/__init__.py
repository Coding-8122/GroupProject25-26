from flask import Blueprint

# Initialize the user profile blueprint
user_bp = Blueprint('user', __name__)

# Import routes at the bottom to avoid circular dependencies
from app.user import routes