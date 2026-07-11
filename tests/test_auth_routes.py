from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.dependencies import (
    get_auth_service,
    get_user_repository,
)
from api.main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def make_user():
    return SimpleNamespace(
        id="user-123",
        email="test@example.com",
        password_hash="hashed-password",
    )


def clear_overrides():
    app.dependency_overrides.pop(
        get_auth_service,
        None,
    )
    app.dependency_overrides.pop(
        get_user_repository,
        None,
    )


def test_register():
    users = Mock()
    service = Mock()

    users.get_by_email.return_value = None
    users.create_user.return_value = make_user()

    service.hash_password.return_value = (
        "hashed-password"
    )
    service.create_access_token.return_value = (
        "access-token"
    )

    app.dependency_overrides[
        get_user_repository
    ] = lambda: users

    app.dependency_overrides[
        get_auth_service
    ] = lambda: service

    try:
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

    finally:
        clear_overrides()


def test_duplicate_email():
    users = Mock()
    service = Mock()

    users.get_by_email.return_value = make_user()

    app.dependency_overrides[
        get_user_repository
    ] = lambda: users

    app.dependency_overrides[
        get_auth_service
    ] = lambda: service

    try:
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

    finally:
        clear_overrides()


def test_login():
    service = Mock()

    service.authenticate.return_value = make_user()
    service.create_access_token.return_value = (
        "access-token"
    )

    app.dependency_overrides[
        get_auth_service
    ] = lambda: service

    try:
        response = client.post(
            "/auth/login",
            json={
                "email": "test@example.com",
                "password": "Password123",
            },
        )

        assert response.status_code == 200
        assert (
            response.json()["access_token"]
            == "access-token"
        )

    finally:
        clear_overrides()


def test_invalid_credentials():
    service = Mock()
    service.authenticate.return_value = None

    app.dependency_overrides[
        get_auth_service
    ] = lambda: service

    try:
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

    finally:
        clear_overrides()


def test_me_requires_token():
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Authentication required."
    }


def test_me():
    service = Mock()
    service.get_current_user.return_value = make_user()

    app.dependency_overrides[
        get_auth_service
    ] = lambda: service

    try:
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

    finally:
        clear_overrides()


def test_me_rejects_invalid_token():
    service = Mock()
    service.get_current_user.return_value = None

    app.dependency_overrides[
        get_auth_service
    ] = lambda: service

    try:
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

    finally:
        clear_overrides()