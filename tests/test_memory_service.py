from unittest.mock import patch

from services.memory_service import memory_service


@patch(
    "services.memory_service.memory.history"
)
def test_get_history(mock_history):
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

    result = memory_service.get_history(
        "conversation-a"
    )

    assert len(result) == 2
    assert result[0]["role"] == "user"
    assert result[1]["role"] == "assistant"
    assert result[0]["sequence"] == 1
    assert result[1]["sequence"] == 2


@patch(
    "services.memory_service.memory.delete_conversation"
)
def test_delete_conversation(mock_delete):
    mock_delete.return_value = 2

    result = memory_service.delete_conversation(
        "conversation-a"
    )

    assert result == 2