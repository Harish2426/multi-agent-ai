from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.dependencies import (
    get_auth_service,
    get_chat_service,
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
        get_chat_service,
        None,
    )


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
    clear_overrides()

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 401


def test_authenticated_user_can_create_chat():
    enable_auth_override()

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
            "conversation_id": (
                "conversation-new"
            ),
        }

        mock_service.chat.assert_called_once_with(
            message="Hello",
            conversation_id=None,
            user_id="user-123",
        )

    finally:
        clear_overrides()


def test_authenticated_user_can_continue_chat():
    enable_auth_override()

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
        clear_overrides()


def test_user_cannot_use_inaccessible_conversation():
    enable_auth_override()

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
        clear_overrides()


def test_chat_passes_normalized_message():
    enable_auth_override()

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
        clear_overrides()