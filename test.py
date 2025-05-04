from fastapi.testclient import TestClient
from main import app
import random
import string

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_get_users():
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(user["username"] == "testuser" for user in data)

def test_create_user():
    unique_username = ''.join(random.choices(string.ascii_lowercase, k=8))
    unique_email = f"{unique_username}@example.com"
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    response = client.post(
        "/register/",
        json={"username": unique_username, "email": unique_email, "full_name": "New User", "password": "password123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == unique_username
    assert data["email"] == unique_email
    response = client.post(
        "/register/",
        json={"username": unique_username, "email": unique_email, "full_name": "New User", "password": "password123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400

def test_authentication():
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    login_response = client.post(
        "/token",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert login_response.status_code == 401
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_get_current_user():
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_update_user():
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    unique_username = ''.join(random.choices(string.ascii_lowercase, k=8))
    unique_email = f"{unique_username}@example.com"
    response = client.post(
        "/register/",
        json={"username": unique_username, "email": unique_email, "full_name": "New User", "password": "password123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    updated_email = f"{unique_username}_updated@example.com"
    response = client.put(
        f"/users/{user_id}",
        json={"full_name": "Updated User", "email": updated_email},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated User"
    assert data["email"] == updated_email
    response = client.put(
        f"/users/{user_id}",
        json={"email": "invalid_email"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422
    response = client.put(
        f"/users/{user_id}",
        json={"full_name": "Updated User"},
        headers={"Authorization": f"Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_delete_user():
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    unique_username = ''.join(random.choices(string.ascii_lowercase, k=8))
    unique_email = f"{unique_username}@example.com"
    response = client.post(
        "/register/",
        json={"username": unique_username, "email": unique_email, "full_name": "New User", "password": "password123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
