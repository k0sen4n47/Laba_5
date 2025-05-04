import requests
import random
import string

BASE_URL = "http://localhost:8000"

def test_read_main():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200

def test_get_users():
    login_response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = requests.get(
        f"{BASE_URL}/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(user["username"] == "testuser" for user in data)

def test_create_user():
    unique_username = ''.join(random.choices(string.ascii_lowercase, k=8))
    unique_email = f"{unique_username}@example.com"

    login_response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = requests.post(
        f"{BASE_URL}/register/",
        json={"username": unique_username, "email": unique_email, "full_name": "New User", "password": "password123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == unique_username
    assert data["email"] == unique_email

    response = requests.post(
        f"{BASE_URL}/register/",
        json={"username": unique_username, "email": unique_email, "full_name": "New User", "password": "password123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400

def test_authentication():
    login_response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    login_response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert login_response.status_code == 401

    response = requests.get(
        f"{BASE_URL}/users/",
        headers={"Authorization": f"Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_get_current_user():
    login_response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

if __name__ == "__main__":
    test_read_main()
    test_authentication()
    test_get_users()
    test_create_user()
    test_get_current_user()
    print("All production tests passed!") 