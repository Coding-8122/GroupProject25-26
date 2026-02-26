from flask import Blueprint

# 1. Define the blueprint FIRST
main_bp = Blueprint('main', __name__)

# 2. Import routes at the BOTTOM to avoid circular dependency
from app.main import routes