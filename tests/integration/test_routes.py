import pytest
from app.models.workout import WorkoutLog
from app.models.body_metric import BodyMetric

def test_dashboard_access_unauthenticated(client):
    """Ensure unauthenticated users are redirected to login."""
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_dashboard_access_authenticated(authenticated_client):
    """Ensure authenticated users can access the dashboard."""
    response = authenticated_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Global Recovery Status' in response.data

def test_add_workout_authenticated(authenticated_client, app):
    """Test logging a new workout via the application form."""
    response = authenticated_client.post('/workouts', data={
        'exercise_name': 'Bench Press',
        'muscle_group': 'Chest',
        'intensity': 8,
        'sets': 3,
        'reps': 10,
        'weight': 60
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Workout logged successfully' in response.data

    with app.app_context():
        workout = WorkoutLog.query.filter_by(exercise_name='Bench Press').first()
        assert workout is not None
        assert workout.intensity == 8
        assert workout.volume == 1800.0

def test_add_body_metrics_authenticated(authenticated_client, app):
    """Test logging daily body weight and fat percentage."""
    response = authenticated_client.post('/metrics', data={
        'date': '2025-01-01',
        'weight': 80.5,
        'body_fat': 14.2
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Body metrics saved successfully' in response.data

    with app.app_context():
        metric = BodyMetric.query.filter_by(weight=80.5).first()
        assert metric is not None
        assert metric.body_fat == 14.2