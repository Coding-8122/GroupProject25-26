# app/models/body_metric.py
from app.extensions import db
from datetime import datetime

class BodyMetric(db.Model):
    """Stores daily weight and body fat metrics."""
    __tablename__ = 'body_metrics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    body_fat = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<BodyMetric {self.date} - {self.weight}kg>'