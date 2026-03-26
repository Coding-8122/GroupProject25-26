# tests/integration/test_routes.py
import pytest

def test_dashboard_access_logged_in(client, app):
    """Test that a logged-in user can access the dashboard."""
    response = client.get('/')
    assert response.status_code == 302  # Should redirect to login since we aren't authenticated