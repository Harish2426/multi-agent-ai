from unittest.mock import patch

from services.memory_service import memory_service


@patch(
    "services.memory_service.memory.history"
)
def test_get_history(mock_history):
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

    result = memory_service.get_history(
        "conversation-a"
    )

    mock_history.assert_called_once_with(
        conversation_id="conversation-a"
    )

    assert len(result) == 1
    assert result[0]["id"] == "memory-1"


@patch(
    "services.memory_service.memory.delete_conversation"
)
def test_delete_conversation(mock_delete):
    mock_delete.return_value = 3

    result = memory_service.delete_conversation(
        "conversation-a"
    )

    mock_delete.assert_called_once_with(
        conversation_id="conversation-a"
    )

    assert result == 3