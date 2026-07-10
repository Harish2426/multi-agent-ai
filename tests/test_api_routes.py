from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from api.routes.auth_routes import get_current_user


client = TestClient(app)

TEST_USER = SimpleNamespace(
    id="user-123",
    email="test@example.com",
)


def override_current_user():
    return TEST_USER


def setup_function():
    app.dependency_overrides[
        get_current_user
    ] = override_current_user


def teardown_function():
    app.dependency_overrides.clear()


@patch(
    "api.routes.conversation_routes."
    "conversation_service.get_history"
)
def test_history_endpoint(mock_history):
    mock_history.return_value = [
        {
            "id": "message-1",
            "role": "user",
            "content": "Hello",
            "timestamp": "2026-07-05T10:00:00+00:00",
            "sequence": 1,
        },
        {
            "id": "message-2",
            "role": "assistant",
            "content": "Hi",
            "timestamp": "2026-07-05T10:00:00+00:00",
            "sequence": 2,
        },
    ]

    response = client.get(
        "/conversations/conversation-a/history"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["conversation_id"] == "conversation-a"
    assert len(body["history"]) == 2
    assert body["history"][0]["role"] == "user"
    assert body["history"][1]["role"] == "assistant"

    mock_history.assert_called_once_with(
        "conversation-a",
        user_id="user-123",
    )


@patch(
    "api.routes.conversation_routes."
    "conversation_service.delete_conversation"
)
def test_delete_endpoint(mock_delete):
    mock_delete.return_value = 2

    response = client.delete(
        "/conversations/conversation-a"
    )

    assert response.status_code == 200

    assert response.json() == {
        "conversation_id": "conversation-a",
        "deleted_count": 2,
    }

    mock_delete.assert_called_once_with(
        "conversation-a",
        user_id="user-123",
    )


def test_conversations_require_authentication():
    app.dependency_overrides.clear()

    response = client.get("/conversations")

    assert response.status_code == 401