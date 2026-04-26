def test_create_user_success(client, test_user):
    client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/users", json={
        "email": "newuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"


def test_create_user_duplicate_email(client, test_user):
    client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/users", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
