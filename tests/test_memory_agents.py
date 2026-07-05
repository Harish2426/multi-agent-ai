from unittest.mock import patch

from app.agents.memory_retriever import memory_retriever
from app.agents.memory_saver import memory_saver


def create_state(
    route: str = "planner",
    conversation_id: str = "conversation-a",
) -> dict:

    return {
        "user_input": "Help me build a FastAPI project",
        "conversation_id": conversation_id,
        "messages": [],
        "route": route,
        "plan": "",
        "research": "",
        "code": "",
        "review": "",
        "tool_result": "",
        "memories": [],
        "final_answer": "Example final response",
    }


@patch(
    "app.agents.memory_retriever.memory.search"
)
def test_memory_retriever(mock_search):

    mock_search.return_value = [
        "Previous FastAPI conversation"
    ]

    state = create_state()

    result = memory_retriever.run(state)

    mock_search.assert_called_once_with(
        conversation_id="conversation-a",
        query=state["user_input"],
    )

    assert result["memories"] == [
        "Previous FastAPI conversation"
    ]


@patch(
    "app.agents.memory_saver.memory.add"
)
def test_memory_saver(mock_add):

    state = create_state()

    memory_saver.run(state)

    mock_add.assert_called_once_with(
        conversation_id="conversation-a",
        user_input=state["user_input"],
        assistant_response=state["final_answer"],
    )


@patch(
    "app.agents.memory_saver.memory.add"
)
def test_different_conversation_id_is_used(
    mock_add,
):

    state = create_state(
        conversation_id="conversation-b"
    )

    memory_saver.run(state)

    assert (
        mock_add.call_args.kwargs[
            "conversation_id"
        ]
        == "conversation-b"
    )


@patch(
    "app.agents.memory_saver.memory.add"
)
def test_calculator_is_not_saved(mock_add):

    state = create_state(
        route="calculator"
    )

    memory_saver.run(state)

    mock_add.assert_not_called()