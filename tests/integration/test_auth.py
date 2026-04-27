import pytest
from app.models.user import User
from app.extensions import db


def test_user_registration(client, app):
    """Test user registration endpoint using the correct auth blueprint prefix."""
    response = client.post('/auth/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None


def test_user_login(client, app):
    """Test user login endpoint using the correct auth blueprint prefix."""
    with app.app_context():
        user = User(email="login@example.com")
        user.set_password("mypassword")
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'login@example.com',
        'password': 'mypassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logout' in response.data