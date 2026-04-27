from app.extensions import db
from datetime import datetime, timezone

class RecoveryLog(db.Model):
    __tablename__ = 'recovery_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Using lambda ensures the time is evaluated at insertion, not at application startup
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), nullable=False)

    # Core recovery metrics
    sleep_hours = db.Column(db.Float, nullable=False)
    muscle_soreness = db.Column(db.Integer, nullable=False)
    energy_level = db.Column(db.Integer, nullable=False)
    stress_level = db.Column(db.Integer, nullable=False)

    # Calculated recovery estimation
    recovery_estimated = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        # Privacy: Do not expose user_id in logs/tracebacks
        return f'<RecoveryLog {self.date}>'