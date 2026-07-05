from unittest.mock import patch

from services.chat_service import chat_service


@patch(
    "services.chat_service.graph.invoke"
)
def test_existing_conversation_id_is_preserved(
    mock_invoke,
):
    mock_invoke.return_value = {
        "final_answer": "Hello",
        "route": "planner",
        "messages": [],
    }

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
    mock_invoke.return_value = {
        "final_answer": "Hello",
        "route": "planner",
        "messages": [],
    }

    result = chat_service.chat(
        message="Hello"
    )

    assert result["conversation_id"]