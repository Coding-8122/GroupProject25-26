import pytest
from app.models.user import User
from app.models.workout import WorkoutLog


def test_user_password_hashing():
    """Ensure passwords are hashed properly and check correctly."""
    user = User(email="test@example.com")
    user.set_password("securepassword123")

    assert user.password_hash is not None
    assert user.password_hash != "securepassword123"
    assert user.check_password("securepassword123") is True
    assert user.check_password("wrongpassword") is False


def test_workout_volume_property():
    """Ensure the volume property calculates total weight lifted correctly."""
    workout = WorkoutLog(sets=3, reps=10, weight=50.0)
    assert workout.volume == 1500.0