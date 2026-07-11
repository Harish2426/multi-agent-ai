from types import SimpleNamespace
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from api.dependencies import get_chat_service
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


def override_auth():
    patcher = patch(
        "api.routes.auth_routes."
        "auth_service.get_current_user"
    )

    mock_get_user = patcher.start()
    mock_get_user.return_value = TEST_USER

    return patcher


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


def test_authenticated_user_can_create_chat():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.return_value = (
        successful_chat_result(
            "conversation-new"
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

        assert response.status_code == 200

        assert response.json() == {
            "response": "Hello from AI",
            "route": "planner",
            "messages": [],
            "conversation_id": "conversation-new",
        }

        mock_service.chat.assert_called_once_with(
            message="Hello",
            conversation_id=None,
            user_id="user-123",
        )

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()


def test_authenticated_user_can_continue_chat():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.return_value = (
        successful_chat_result(
            "conversation-123"
        )
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Continue",
                "conversation_id": (
                    "conversation-123"
                ),
            },
            headers=auth_headers(),
        )

        assert response.status_code == 200

        mock_service.chat.assert_called_once_with(
            message="Continue",
            conversation_id="conversation-123",
            user_id="user-123",
        )

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()


def test_user_cannot_use_inaccessible_conversation():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.side_effect = PermissionError(
        "Conversation not found."
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "conversation_id": (
                    "foreign-conversation"
                ),
            },
            headers=auth_headers(),
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Conversation not found."
        }

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()


def test_chat_passes_normalized_message():
    auth_patcher = override_auth()

    mock_service = Mock()
    mock_service.chat.return_value = (
        successful_chat_result(
            "conversation-new"
        )
    )

    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service

    try:
        response = client.post(
            "/chat",
            json={
                "message": "   Hello   ",
            },
            headers=auth_headers(),
        )

        assert response.status_code == 200

        mock_service.chat.assert_called_once_with(
            message="Hello",
            conversation_id=None,
            user_id="user-123",
        )

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
        auth_patcher.stop()