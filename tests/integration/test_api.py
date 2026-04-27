import pytest


def test_weight_api_json_structure(authenticated_client):
    """Verify that weight API returns correct JSON for Chart.js."""
    authenticated_client.post(
        "/metrics", data={"date": "2026-04-09", "weight": 80.0, "body_fat": 15.0}
    )

    response = authenticated_client.get("/api/stats/weight")
    assert response.status_code == 200
    data = response.get_json()
    assert "labels" in data
    assert data["weight"][0] == 80.0


def test_volume_api_aggregation(authenticated_client):
    """Ensure workout volume is correctly aggregated by muscle group."""
    authenticated_client.post(
        "/workouts",
        data={
            "exercise_name": "Squat",
            "muscle_group": "Legs",
            "intensity": 9,
            "sets": 3,
            "reps": 10,
            "weight": 100,
        },
    )

    response = authenticated_client.get("/api/stats/volume")
    data = response.get_json()
    assert "Legs" in data["labels"]
    assert data["data"][data["labels"].index("Legs")] == 3000.0
