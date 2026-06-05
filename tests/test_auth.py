"""
Authentication Test Suite
Verifies user registration, login workflows, and edge cases like duplicate users
and invalid credentials.
"""
import pytest
from app.app import create_app

@pytest.fixture
def client():
    """Creates a fresh test client and isolates the test environment."""
    app = create_app({"TESTING": True})
    
    # Reset the in-memory user database for predictable testing
    from app.routes.auth_routes import auth_service
    auth_service.users_db.clear()
    
    with app.test_client() as client:
        yield client

def test_register_success(client):
    """Test successful user registration."""
    response = client.post('/auth/register', json={
        "username": "testuser",
        "password": "securepassword123"
    })
    assert response.status_code == 201
    assert response.json["success"] is True

def test_register_duplicate_user(client):
    """Test that duplicate usernames are rejected with a 409 Conflict."""
    client.post('/auth/register', json={
        "username": "testuser",
        "password": "securepassword123"
    })
    response = client.post('/auth/register', json={
        "username": "testuser",
        "password": "differentpassword"
    })
    assert response.status_code == 409
    assert response.json["error"]["code"] == "CONFLICT"

def test_login_success(client):
    """Test successful login and JWT generation."""
    client.post('/auth/register', json={
        "username": "testuser",
        "password": "securepassword123"
    })
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json["data"]
    assert "refresh_token" in response.json["data"]

def test_login_invalid_credentials(client):
    """Test login failure with incorrect password."""
    client.post('/auth/register', json={
        "username": "testuser",
        "password": "securepassword123"
    })
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json["error"]["code"] == "UNAUTHORIZED"