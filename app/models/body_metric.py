from datetime import datetime, timezone
from app.extensions import db

class BodyMetric(db.Model):
    __tablename__ = 'body_metrics'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    body_fat = db.Column(db.Float)