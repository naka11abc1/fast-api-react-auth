def test_login_success(client, test_user):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "access_token" in response.cookies


def test_login_wrong_password(client, test_user):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_wrong_email(client):
    response = client.post("/auth/login", json={
        "email": "notfound@example.com",
        "password": "password123"
    })
    assert response.status_code == 401


def test_get_auth_user_authenticated(client, test_user):
    client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.get("/auth/user")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_auth_user_unauthenticated(client):
    response = client.get("/auth/user")
    assert response.status_code == 401


def test_logout(client, test_user):
    client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/auth/logout")
    assert response.status_code == 200
