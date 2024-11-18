import os
import tempfile
import pytest
from app import create_app, db
from app.models.user import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = tempfile.mkdtemp()

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(app, client):
    """A test client with authentication."""
    with app.app_context():
        user = User(
            username='test_user',
            email='test@example.com',
            full_name='Test User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        client.post('/auth/login', data={
            'username': 'test_user',
            'password': 'password123'
        }, follow_redirects=True)
        
        return client
