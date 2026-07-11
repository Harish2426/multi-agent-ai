from types import SimpleNamespace
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from api.dependencies import get_chat_service
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


def override_auth():
    patcher = patch(
        "api.routes.auth_routes."
        "auth_service.get_current_user"
    )

    mock_get_user = patcher.start()
    mock_get_user.return_value = TEST_USER

    return patcher


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
    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 401


def test_empty_message_is_rejected():
    auth_patcher = override_auth()

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
        auth_patcher.stop()


def test_quota_error_returns_503():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.side_effect = ModelQuotaError(
        "quota exhausted"
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

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
            "detail": "AI model quota is unavailable."
        }

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()


def test_model_unavailable_returns_503():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.side_effect = (
        ModelUnavailableError(
            "service unavailable"
        )
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
            },
            headers=auth_headers(),
        )

        assert response.status_code == 503

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()


def test_unexpected_error_is_safe():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.side_effect = RuntimeError(
        "secret internal database details"
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

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
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()