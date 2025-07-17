import pytest


def test_register_and_login(client):
    user_payload = {
        "email": "user@example.com",
        "password": "secret123"
    }

    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_payload["email"]
    assert "id" in data

    # Повторная регистрация — ошибка
    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"

    # Вход
    response = client.post("/auth/login", json=user_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert "accessToken" in token_data
    assert token_data["tokenType"] == "bearer"


def test_me(client):
    email = "me@example.com"
    password = "testpass"

    client.post("/auth/register", json={"email": email, "password": password})
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200
    token = login_response.json()["accessToken"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == email


def test_me_unauthorized(client):
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)


def test_login_wrong_password(client):
    email = "wrongpass@example.com"
    password = "correctpass"
    wrong_password = "wrongpass"

    client.post("/auth/register", json={"email": email, "password": password})

    response = client.post("/auth/login", json={"email": email, "password": wrong_password})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.parametrize(
    "payload, error_field",
    [
        ({"email": "", "password": "secret123"}, "email"),
        ({"email": "invalid-email", "password": "secret123"}, "email"),
        ({"email": "test@example.com", "password": ""}, "password"),
        ({"email": "test@example.com", "password": "123"}, "password"),
    ],
)
def test_register_invalid_data(client, payload, error_field):
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422
    errors = response.json().get("detail", [])
    assert any(error_field in str(e.get("loc", [])) for e in errors)


def test_me_invalid_token(client):
    invalid_token = "Bearer invalid.token.value"
    response = client.get("/auth/me", headers={"Authorization": invalid_token})
    assert response.status_code in (401, 403)
