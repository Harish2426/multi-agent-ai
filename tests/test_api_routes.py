from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


@patch(
    "api.routes.memory_service.get_history"
)
def test_history_endpoint(mock_history):
    mock_history.return_value = [
        {
            "id": "memory-1",
            "document": (
                "User: Hello\n"
                "Assistant: Hi"
            ),
            "metadata": {
                "conversation_id": "conversation-a",
                "user_input": "Hello",
            },
        }
    ]

    response = client.get(
        "/conversations/conversation-a/history"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["conversation_id"] == "conversation-a"
    assert len(body["history"]) == 1


@patch(
    "api.routes.memory_service.delete_conversation"
)
def test_delete_endpoint(mock_delete):
    mock_delete.return_value = 2

    response = client.delete(
        "/conversations/conversation-a"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["conversation_id"] == "conversation-a"
    assert body["deleted_count"] == 2