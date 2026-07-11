from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.dependencies import (
    get_auth_service,
    get_conversation_service,
)
from api.main import app


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
        get_conversation_service,
        None,
    )


def test_history_endpoint():
    enable_auth_override()

    mock_service = Mock()

    mock_service.get_history.return_value = [
        {
            "id": "message-1",
            "role": "user",
            "content": "Hello",
            "timestamp": (
                "2026-07-05T10:00:00+00:00"
            ),
            "sequence": 1,
        },
        {
            "id": "message-2",
            "role": "assistant",
            "content": "Hi",
            "timestamp": (
                "2026-07-05T10:00:00+00:00"
            ),
            "sequence": 2,
        },
    ]

    app.dependency_overrides[
        get_conversation_service
    ] = lambda: mock_service

    try:
        response = client.get(
            "/conversations/"
            "conversation-a/history",
            headers=auth_headers(),
        )

        assert response.status_code == 200

        body = response.json()

        assert (
            body["conversation_id"]
            == "conversation-a"
        )

        assert len(body["history"]) == 2

        assert (
            body["history"][0]["role"]
            == "user"
        )

        assert (
            body["history"][1]["role"]
            == "assistant"
        )

        mock_service.get_history.assert_called_once_with(
            "conversation-a",
            user_id="user-123",
        )

    finally:
        clear_overrides()


def test_delete_endpoint():
    enable_auth_override()

    mock_service = Mock()

    mock_service.delete_conversation.return_value = 2

    app.dependency_overrides[
        get_conversation_service
    ] = lambda: mock_service

    try:
        response = client.delete(
            "/conversations/conversation-a",
            headers=auth_headers(),
        )

        assert response.status_code == 200

        body = response.json()

        assert (
            body["conversation_id"]
            == "conversation-a"
        )

        assert body["deleted_count"] == 2

        (
            mock_service
            .delete_conversation
            .assert_called_once_with(
                "conversation-a",
                user_id="user-123",
            )
        )

    finally:
        clear_overrides()