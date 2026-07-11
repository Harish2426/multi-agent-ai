from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.dependencies import (
    get_auth_service,
    get_chat_service,
)
from api.main import app
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


def auth_headers():
    return {
        "Authorization": "Bearer test-token",
    }


def enable_auth_override():
    mock_auth_service = Mock()

    mock_auth_service.get_current_user.return_value = (
        TEST_USER
    )

    app.dependency_overrides[
        get_auth_service
    ] = lambda: mock_auth_service

    return mock_auth_service


def clear_overrides():
    app.dependency_overrides.pop(
        get_auth_service,
        None,
    )

    app.dependency_overrides.pop(
        get_chat_service,
        None,
    )


def test_health():
    clear_overrides()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_readiness():
    clear_overrides()

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": "available",
    }


def test_chat_requires_authentication():
    clear_overrides()

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
            },
            headers=auth_headers(),
        )

        assert response.status_code == 422

    finally:
        clear_overrides()


def test_quota_error_returns_503():
    enable_auth_override()

    mock_chat_service = Mock()

    mock_chat_service.chat.side_effect = (
        ModelQuotaError(
            "quota exhausted"
        )
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_chat_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
            headers=auth_headers(),
        )

        assert response.status_code == 503

        assert response.json() == {
            "detail": (
                "AI model quota is unavailable."
            )
        }

    finally:
        clear_overrides()


def test_model_unavailable_returns_503():
    enable_auth_override()

    mock_chat_service = Mock()

    mock_chat_service.chat.side_effect = (
        ModelUnavailableError(
            "service unavailable"
        )
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_chat_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
            headers=auth_headers(),
        )

        assert response.status_code == 503

        assert response.json() == {
            "detail": "AI model is unavailable."
        }

    finally:
        clear_overrides()


def test_unexpected_error_is_safe():
    enable_auth_override()

    mock_chat_service = Mock()

    mock_chat_service.chat.side_effect = (
        RuntimeError(
            "secret internal database details"
        )
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_chat_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
            headers=auth_headers(),
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
        clear_overrides()