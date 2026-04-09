import pytest
from app.models.workout import WorkoutLog


def test_add_workout_success(authenticated_client, app):
    """Test logging a workout exercise and database persistence."""
    res = authenticated_client.post(
        "/workouts",
        data={
            "exercise_name": "Deadlift",
            "muscle_group": "Back",
            "intensity": 10,
            "sets": 1,
            "reps": 1,
            "weight": 200,
        },
        follow_redirects=True,
    )

    assert b"Workout logged successfully" in res.data
    with app.app_context():
        assert WorkoutLog.query.filter_by(exercise_name="Deadlift").first() is not None
