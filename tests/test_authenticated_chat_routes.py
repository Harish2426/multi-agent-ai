from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

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


def successful_chat_result(
    conversation_id: str,
):
    return {
        "response": "Hello from AI",
        "route": "planner",
        "messages": [],
        "conversation_id": conversation_id,
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
    "api.routes.chat_routes."
    "chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_authenticated_user_can_create_chat(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.return_value = successful_chat_result(
        "conversation-new"
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Hello from AI",
        "route": "planner",
        "messages": [],
        "conversation_id": "conversation-new",
    }

    mock_chat.assert_called_once_with(
        message="Hello",
        conversation_id=None,
        user_id="user-123",
    )


@patch(
    "api.routes.chat_routes."
    "chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_authenticated_user_can_continue_chat(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.return_value = successful_chat_result(
        "conversation-123"
    )

    response = client.post(
        "/chat",
        json={
            "message": "Continue",
            "conversation_id": "conversation-123",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200

    mock_chat.assert_called_once_with(
        message="Continue",
        conversation_id="conversation-123",
        user_id="user-123",
    )


@patch(
    "api.routes.chat_routes."
    "chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_user_cannot_use_inaccessible_conversation(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.side_effect = PermissionError(
        "Conversation not found."
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "conversation_id": "foreign-conversation",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Conversation not found."
    }


@patch(
    "api.routes.chat_routes."
    "chat_service.chat"
)
@patch(
    "api.routes.auth_routes."
    "auth_service.get_current_user"
)
def test_chat_passes_normalized_message(
    mock_get_current_user,
    mock_chat,
):
    mock_get_current_user.return_value = TEST_USER

    mock_chat.return_value = successful_chat_result(
        "conversation-new"
    )

    response = client.post(
        "/chat",
        json={
            "message": "   Hello   ",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200

    mock_chat.assert_called_once_with(
        message="Hello",
        conversation_id=None,
        user_id="user-123",
    )