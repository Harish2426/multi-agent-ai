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


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


@patch("api.routes.memory.collection.count")
def test_readiness(mock_count):
    mock_count.return_value = 0

    response = client.get("/ready")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "memory": "available",
    }


def test_empty_message_is_rejected():
    response = client.post(
        "/chat",
        json={
            "message": "   ",
            "conversation_id": None,
        },
    )

    assert response.status_code == 422


@patch("api.routes.chat_service.chat")
def test_quota_error_returns_503(mock_chat):
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


@patch("api.routes.chat_service.chat")
def test_model_unavailable_returns_503(
    mock_chat,
):
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


@patch("api.routes.chat_service.chat")
def test_unexpected_error_is_safe(mock_chat):
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