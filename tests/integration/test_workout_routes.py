import pytest
from app.models.workout import WorkoutLog


def test_add_workout_success(authenticated_client, app):
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


def test_export_workouts_authenticated(authenticated_client):
    """Test that the CSV export returns a valid file."""
    # Log a dummy workout to ensure there is data to export
    authenticated_client.post(
        "/workouts",
        data={
            "exercise_name": "ExportTest",
            "muscle_group": "Arms",
            "intensity": 5,
            "sets": 1,
            "reps": 1,
            "weight": 10,
        },
    )

    response = authenticated_client.get("/export/workouts")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"ExportTest" in response.data
