from app.extensions import db
from datetime import datetime

class RecoveryLog(db.Model):
    __tablename__ = 'recovery_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)

    # Core recovery metrics
    sleep_hours = db.Column(db.Float, nullable=False)
    muscle_soreness = db.Column(db.Integer, nullable=False)  
    energy_level = db.Column(db.Integer, nullable=False)  
    stress_level = db.Column(db.Integer, nullable=False)  

    # The result of your logic calculation
    recovery_estimated = db.Column(db.Integer, nullable=True) 

    def __repr__(self):
        return f'<RecoveryLog {self.date} - User {self.user_id}>'