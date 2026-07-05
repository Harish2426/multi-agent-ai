from unittest.mock import patch

from app.agents.memory_retriever import memory_retriever
from app.agents.memory_saver import memory_saver


def create_state(
    route: str = "planner",
) -> dict:

    return {
        "user_input": "Help me build a FastAPI project",
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

    assert result["memories"] == [
        "Previous FastAPI conversation"
    ]

    assert (
        "Memory retrieved: 1 item(s)"
        in result["messages"]
    )


@patch(
    "app.agents.memory_retriever.memory.search"
)
def test_memory_retrieval_failure(
    mock_search,
):

    mock_search.side_effect = RuntimeError(
        "database unavailable"
    )

    state = create_state()

    result = memory_retriever.run(state)

    assert result["memories"] == []

    assert (
        "Memory retrieval unavailable."
        in result["messages"]
    )


@patch(
    "app.agents.memory_saver.memory.add"
)
def test_memory_saver(mock_add):

    state = create_state()

    result = memory_saver.run(state)

    mock_add.assert_called_once_with(
        user_input=state["user_input"],
        assistant_response=state["final_answer"],
    )

    assert (
        "Conversation saved to memory."
        in result["messages"]
    )


@patch(
    "app.agents.memory_saver.memory.add"
)
def test_calculator_is_not_saved(
    mock_add,
):

    state = create_state(
        route="calculator"
    )

    memory_saver.run(state)

    mock_add.assert_not_called()