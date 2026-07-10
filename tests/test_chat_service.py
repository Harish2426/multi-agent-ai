from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.chat_service import chat_service


GRAPH_RESULT = {
    "final_answer": "Hello",
    "route": "planner",
    "messages": [],
}


@patch(
    "services.chat_service.graph.invoke"
)
def test_existing_conversation_id_is_preserved(
    mock_invoke,
):
    mock_invoke.return_value = GRAPH_RESULT

    result = chat_service.chat(
        message="Hello",
        conversation_id="conversation-123",
    )

    assert (
        result["conversation_id"]
        == "conversation-123"
    )


@patch(
    "services.chat_service.graph.invoke"
)
def test_conversation_id_is_generated(
    mock_invoke,
):
    mock_invoke.return_value = GRAPH_RESULT

    result = chat_service.chat(
        message="Hello"
    )

    assert result["conversation_id"]


@patch(
    "services.chat_service."
    "conversation_service.add_assistant_message"
)
@patch(
    "services.chat_service."
    "conversation_service.add_user_message"
)
@patch(
    "services.chat_service."
    "conversation_service.conversations."
    "create_conversation"
)
@patch(
    "services.chat_service.graph.invoke"
)
def test_authenticated_new_chat_is_persisted(
    mock_invoke,
    mock_create,
    mock_add_user,
    mock_add_assistant,
):
    mock_invoke.return_value = GRAPH_RESULT

    result = chat_service.chat(
        message="Hello",
        user_id="user-123",
    )

    conversation_id = result["conversation_id"]

    mock_create.assert_called_once_with(
        conversation_id=conversation_id,
        title="Hello",
        user_id="user-123",
    )

    mock_add_user.assert_called_once_with(
        conversation_id,
        "Hello",
    )

    mock_add_assistant.assert_called_once_with(
        conversation_id=conversation_id,
        content="Hello",
        route="planner",
    )


@patch(
    "services.chat_service."
    "conversation_service.add_assistant_message"
)
@patch(
    "services.chat_service."
    "conversation_service.add_user_message"
)
@patch(
    "services.chat_service."
    "conversation_service.conversations."
    "get_conversation"
)
@patch(
    "services.chat_service.graph.invoke"
)
def test_authenticated_existing_chat_checks_ownership(
    mock_invoke,
    mock_get,
    mock_add_user,
    mock_add_assistant,
):
    mock_invoke.return_value = GRAPH_RESULT

    mock_get.return_value = SimpleNamespace(
        id="conversation-123",
        user_id="user-123",
    )

    chat_service.chat(
        message="Hello",
        conversation_id="conversation-123",
        user_id="user-123",
    )

    mock_get.assert_called_once_with(
        "conversation-123",
        user_id="user-123",
    )

    mock_add_user.assert_called_once_with(
        "conversation-123",
        "Hello",
    )


@patch(
    "services.chat_service."
    "conversation_service.conversations."
    "get_conversation"
)
def test_authenticated_user_cannot_use_foreign_conversation(
    mock_get,
):
    mock_get.return_value = None

    with pytest.raises(PermissionError):
        chat_service.chat(
            message="Hello",
            conversation_id="private-conversation",
            user_id="user-123",
        )


@patch(
    "services.chat_service."
    "conversation_service.delete_conversation"
)
@patch(
    "services.chat_service."
    "conversation_service.add_assistant_message"
)
@patch(
    "services.chat_service."
    "conversation_service.add_user_message"
)
@patch(
    "services.chat_service."
    "conversation_service.conversations."
    "create_conversation"
)
@patch(
    "services.chat_service.graph.invoke"
)
def test_failed_new_chat_is_cleaned_up(
    mock_invoke,
    mock_create,
    mock_add_user,
    mock_add_assistant,
    mock_delete,
):
    mock_invoke.side_effect = RuntimeError(
        "model failed"
    )

    with pytest.raises(RuntimeError):
        chat_service.chat(
            message="Hello",
            user_id="user-123",
        )

    mock_create.assert_called_once()

    mock_add_user.assert_not_called()
    mock_add_assistant.assert_not_called()

    created_conversation_id = (
        mock_create.call_args.kwargs[
            "conversation_id"
        ]
    )

    mock_delete.assert_called_once_with(
        created_conversation_id,
        user_id="user-123",
    )


@patch(
    "services.chat_service."
    "conversation_service.add_assistant_message"
)
@patch(
    "services.chat_service."
    "conversation_service.add_user_message"
)
@patch(
    "services.chat_service."
    "conversation_service.conversations."
    "get_conversation"
)
@patch(
    "services.chat_service.graph.invoke"
)
def test_failed_existing_chat_adds_no_messages(
    mock_invoke,
    mock_get,
    mock_add_user,
    mock_add_assistant,
):
    mock_get.return_value = SimpleNamespace(
        id="conversation-123",
        user_id="user-123",
    )

    mock_invoke.side_effect = RuntimeError(
        "model failed"
    )

    with pytest.raises(RuntimeError):
        chat_service.chat(
            message="Hello",
            conversation_id="conversation-123",
            user_id="user-123",
        )

    mock_add_user.assert_not_called()
    mock_add_assistant.assert_not_called()