from app.extensions import db
from datetime import datetime


class RecoveryLog(db.Model):
    __tablename__ = 'recovery_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date, index=True)

    # Recovery Metrics
    sleep_hours = db.Column(db.Float, nullable=False)
    stress_level = db.Column(db.Integer)  # 1-10
    muscle_soreness = db.Column(db.Integer)  # 1-10
    hrv = db.Column(db.Integer)  # Heart Rate Variability

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f'<RecoveryLog {self.date} - User {self.user_id}>'