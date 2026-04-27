from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    gender = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    height = db.Column(db.Float) # cm
    weight = db.Column(db.Float) # kg

    def set_password(self, password):
        """Hashes the password for secure storage."""
        self.password_hash = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'