import pytest
from app.models.user import User
from app.models.workout import WorkoutLog

def test_user_password_hashing():
    """Ensure passwords are correctly hashed and verified."""
    user = User(email="model@example.com")
    user.set_password("secure_pass")
    assert user.password_hash != "secure_pass"
    assert user.check_password("secure_pass") is True

def test_workout_volume_calculation():
    """Test the @property volume calculation in WorkoutLog model."""
    workout = WorkoutLog(sets=3, reps=10, weight=60.0)
    assert workout.volume == 1800.0