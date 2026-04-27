import pytest
from app.models.workout import WorkoutLog


def test_add_workout_authenticated(authenticated_client, app):
    """Ensure that an authenticated user can log a workout exercise."""
    response = authenticated_client.post(
        "/workouts",
        data={
            "exercise_name": "Bench Press",
            "muscle_group": "Chest",
            "intensity": 8,
            "sets": 3,
            "reps": 10,
            "weight": 60,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert b"Workout logged successfully" in response.data

    with app.app_context():
        workout = WorkoutLog.query.filter_by(exercise_name="Bench Press").first()
        assert workout is not None
        assert workout.intensity == 8
        assert workout.muscle_group == "Chest"
