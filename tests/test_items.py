"""
Item Resource Test Suite
Verifies CRUD operations and ensures JWT authentication is strictly enforced
on protected endpoints.
"""
import pytest
from app.app import create_app

@pytest.fixture
def client():
    """Creates a test client and resets in-memory databases."""
    app = create_app({"TESTING": True})
    
    # Reset both data stores for clean test state
    from app.routes.auth_routes import auth_service
    from app.routes.item_routes import item_service
    auth_service.users_db.clear()
    item_service.repository.db.clear()
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    """Helper to generate a valid JWT header for protected route tests."""
    client.post('/auth/register', json={"username": "testuser", "password": "password123"})
    response = client.post('/auth/login', json={"username": "testuser", "password": "password123"})
    token = response.json["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_items_empty(client):
    """Test retrieving items when the database is empty (Public)."""
    response = client.get('/items')
    assert response.status_code == 200
    assert response.json["data"] == []

def test_create_item_unauthorized(client):
    """Test that creating an item without a JWT fails with 401."""
    response = client.post('/items', json={"name": "Test Item"})
    assert response.status_code == 401
    assert response.json["error"]["code"] == "UNAUTHORIZED"

def test_create_and_get_item(client, auth_headers):
    """Test full creation and retrieval lifecycle."""
    # Create
    post_res = client.post('/items', json={
        "name": "Server Node 1",
        "description": "Primary database node"
    }, headers=auth_headers)
    
    assert post_res.status_code == 201
    assert post_res.json["data"]["name"] == "Server Node 1"
    
    item_id = post_res.json["data"]["id"]
    
    # Read
    get_res = client.get(f'/items/{item_id}')
    assert get_res.status_code == 200
    assert get_res.json["data"]["id"] == item_id

def test_update_item(client, auth_headers):
    """Test updating an existing item."""
    post_res = client.post('/items', json={"name": "Old Name"}, headers=auth_headers)
    item_id = post_res.json["data"]["id"]
    
    put_res = client.put(f'/items/{item_id}', json={"name": "New Name"}, headers=auth_headers)
    assert put_res.status_code == 200
    assert put_res.json["data"]["name"] == "New Name"

def test_delete_item(client, auth_headers):
    """Test deleting an item and verifying it is gone."""
    post_res = client.post('/items', json={"name": "To Delete"}, headers=auth_headers)
    item_id = post_res.json["data"]["id"]
    
    # Delete
    del_res = client.delete(f'/items/{item_id}', headers=auth_headers)
    assert del_res.status_code == 200
    
    # Verify not found
    get_res = client.get(f'/items/{item_id}')
    assert get_res.status_code == 404
    assert get_res.json["error"]["code"] == "RESOURCE_NOT_FOUND"