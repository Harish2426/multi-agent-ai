from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def make_user():
    return SimpleNamespace(
        id="user-123",
        email="test@example.com",
        password_hash="hashed-password",
    )


@patch(
    "api.routes.auth_routes."
    "auth_service.create_access_token"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.hash_password"
)
@patch(
    "api.routes.auth_routes."
    "user_repository.create_user"
)
@patch(
    "api.routes.auth_routes."
    "user_repository.get_by_email"
)
def test_register(
    mock_get_by_email,
    mock_create_user,
    mock_hash_password,
    mock_create_access_token,
):
    mock_get_by_email.return_value = None
    mock_hash_password.return_value = "hashed-password"
    mock_create_user.return_value = make_user()
    mock_create_access_token.return_value = "access-token"

    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "access_token": "access-token",
        "token_type": "bearer",
        "user": {
            "id": "user-123",
            "email": "test@example.com",
        },
    }


@patch(
    "api.routes.auth_routes."
    "user_repository.get_by_email"
)
def test_duplicate_email(mock_get_by_email):
    mock_get_by_email.return_value = make_user()

    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Email already exists."
    }


@patch(
    "api.routes.auth_routes."
    "auth_service.create_access_token"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.authenticate"
)
def test_login(
    mock_authenticate,
    mock_create_access_token,
):
    mock_authenticate.return_value = make_user()
    mock_create_access_token.return_value = "access-token"

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "access-token"


@patch(
    "api.routes.auth_routes."
    "auth_service.authenticate"
)
def test_invalid_credentials(mock_authenticate):
    mock_authenticate.return_value = None

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials."
    }


def test_me_requires_token():
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Authentication required."
    }


@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_me(mock_get_current_user):
    mock_get_current_user.return_value = make_user()

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer valid-token",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "user-123",
        "email": "test@example.com",
    }


@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_me_rejects_invalid_token(
    mock_get_current_user,
):
    mock_get_current_user.return_value = None

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or expired token."
    }