import pytest
from app.models.user import User
from app.extensions import db


def test_registration_flow(client, app):
    """Test successful user registration and redirection."""
    response = client.post(
        "/auth/register",
        data={
            "email": "new@example.com",
            "password": "password123",
            "confirm_password": "password123",
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
    """Test login credentials and session termination."""
    with app.app_context():
        u = User(email="login@test.com")
        u.set_password("pass")
        db.session.add(u)
        db.session.commit()

    # Login
    res = client.post(
        "/auth/login",
        data={"email": "login@test.com", "password": "pass"},
        follow_redirects=True,
    )
    assert b"Logout" in res.data

    # Logout
    res = client.get("/auth/logout", follow_redirects=True)
    assert b"Login" in res.data
