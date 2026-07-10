from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from api.routes.auth_routes import get_current_user
from app.models import (
    ModelQuotaError,
    ModelUnavailableError,
)


client = TestClient(
    app,
    raise_server_exceptions=False,
)


TEST_USER = SimpleNamespace(
    id="user-123",
    email="test@example.com",
)


def override_current_user():
    return TEST_USER


def enable_auth_override():
    app.dependency_overrides[
        get_current_user
    ] = override_current_user


def disable_auth_override():
    app.dependency_overrides.pop(
        get_current_user,
        None,
    )


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_readiness():
    response = client.get("/ready")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "database": "available",
    }


def test_chat_requires_authentication():
    disable_auth_override()

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 401


def test_empty_message_is_rejected():
    enable_auth_override()

    try:
        response = client.post(
            "/chat",
            json={
                "message": "   ",
                "conversation_id": None,
            },
        )

        assert response.status_code == 422

    finally:
        disable_auth_override()


@patch(
    "api.routes.chat_routes.chat_service.chat"
)
def test_quota_error_returns_503(mock_chat):
    enable_auth_override()

    try:
        mock_chat.side_effect = ModelQuotaError(
            "quota exhausted"
        )

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
        )

        assert response.status_code == 503

        assert response.json() == {
            "detail": "AI model quota is unavailable."
        }

    finally:
        disable_auth_override()


@patch(
    "api.routes.chat_routes.chat_service.chat"
)
def test_model_unavailable_returns_503(
    mock_chat,
):
    enable_auth_override()

    try:
        mock_chat.side_effect = ModelUnavailableError(
            "service unavailable"
        )

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
        )

        assert response.status_code == 503

    finally:
        disable_auth_override()


@patch(
    "api.routes.chat_routes.chat_service.chat"
)
def test_unexpected_error_is_safe(mock_chat):
    enable_auth_override()

    try:
        mock_chat.side_effect = RuntimeError(
            "secret internal database details"
        )

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
        )

        assert response.status_code == 500

        assert response.json() == {
            "detail": "Internal server error."
        }

        assert (
            "secret internal database details"
            not in response.text
        )

    finally:
        disable_auth_override()