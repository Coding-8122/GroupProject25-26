import pytest
from app import create_app
from app.extensions import db
from app.models.user import User


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False  # Disable CSRF for testing form submissions
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def authenticated_client(client, app):
    """A test client with a pre-logged in user using a session mock."""
    with app.app_context():
        user = User(email="test@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True
    return client