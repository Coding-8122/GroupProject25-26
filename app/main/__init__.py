from flask import Blueprint

# Initialize the main application blueprint
main_bp = Blueprint('main', __name__)

# Import routes at the bottom to avoid circular dependencies
from app.main import routes