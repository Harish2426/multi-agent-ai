from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

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


@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_empty_message_is_rejected(
    mock_get_current_user,
):
    mock_get_current_user.return_value = TEST_USER

    response = client.post(
        "/chat",
        json={
            "message": "   ",
            "conversation_id": None,
        },
        headers={
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 422


@patch(
    "api.routes.chat_routes.chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_quota_error_returns_503(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.side_effect = ModelQuotaError(
        "quota exhausted"
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
        headers={
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 503

    assert response.json() == {
        "detail": "AI model quota is unavailable."
    }


@patch(
    "api.routes.chat_routes.chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_model_unavailable_returns_503(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.side_effect = ModelUnavailableError(
        "service unavailable"
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
        headers={
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 503


@patch(
    "api.routes.chat_routes.chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_unexpected_error_is_safe(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.side_effect = RuntimeError(
        "secret internal database details"
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
        headers={
            "Authorization": "Bearer test-token",
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