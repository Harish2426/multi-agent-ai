import pytest

from app.graph import graph
from app.models import (
    ModelAuthenticationError,
    ModelQuotaError,
    ModelUnavailableError,
)


pytestmark = pytest.mark.integration


def create_state(message: str) -> dict:
    return {
        "user_input": message,
        "messages": [],
        "route": "",
        "plan": "",
        "research": "",
        "code": "",
        "review": "",
        "tool_result": "",
        "final_answer": "",
    }


def invoke_live_graph(message: str):
    """
    Run the live graph.

    Skip the integration test when the external Gemini service
    cannot be used because of quota, availability, or credentials.
    """

    try:
        return graph.invoke(
            create_state(message)
        )

    except ModelQuotaError as error:
        pytest.skip(
            f"Gemini quota unavailable: {error}"
        )

    except ModelUnavailableError as error:
        pytest.skip(
            f"Gemini service unavailable: {error}"
        )

    except ModelAuthenticationError as error:
        pytest.skip(
            f"Gemini authentication unavailable: {error}"
        )


def test_planner_route():
    result = invoke_live_graph(
        "Create a roadmap for learning FastAPI"
    )

    assert result["route"] == "planner"
    assert result["final_answer"]


def test_researcher_route():
    result = invoke_live_graph(
        "What are the latest developments in AI?"
    )

    assert result["route"] == "researcher"
    assert result["final_answer"]


def test_coder_route():
    result = invoke_live_graph(
        "Write a Python function to check prime numbers"
    )

    assert result["route"] == "coder"
    assert result["final_answer"]


def test_reviewer_route():
    result = invoke_live_graph(
        "Review this Python code for security problems"
    )

    assert result["route"] == "reviewer"
    assert result["final_answer"]