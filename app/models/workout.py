from app.extensions import db
from datetime import datetime, timezone

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Using lambda ensures the time is evaluated at insertion, not at application startup
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(), nullable=False)

    exercise_name = db.Column(db.String(100), nullable=False)

    muscle_group = db.Column(db.String(50), nullable=False, default='Full Body')
    intensity = db.Column(db.Integer, nullable=False, default=5)  # RPE 1-10

    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Weight in kg

    @property
    def volume(self):
        """Calculates total training volume for the entry."""
        return self.sets * self.reps * self.weight

    def __repr__(self):
        return f'<WorkoutLog {self.exercise_name} ({self.muscle_group}) - {self.date}>'