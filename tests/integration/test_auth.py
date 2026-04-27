import pytest
from app.models.user import User
from app.extensions import db


def test_registration_flow(client, app):
    """Test user registration with a strong password."""
    response = client.post(
        "/auth/register",
        data={
            "email": "new@example.com",
            "password": "Password123!",  # Strong password
            "confirm_password": "Password123!",
            "height": 180,
            "weight": 75,
            "birth_date": "1990-01-01",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(email="new@example.com").first() is not None


def test_login_logout_flow(client, app):
    """Test authenticated session cycle."""
    with app.app_context():
        u = User(email="login@test.com")
        u.set_password("Password123!")
        db.session.add(u)
        db.session.commit()

    # Login
    res = client.post(
        "/auth/login",
        data={"email": "login@test.com", "password": "Password123!"},
        follow_redirects=True,
    )
    assert b"Logout" in res.data

    # Logout (POST-only)
    res = client.post("/auth/logout", follow_redirects=True)
    assert b"Login" in res.data
