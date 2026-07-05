from app.graph import graph


def create_state(message: str) -> dict:
    return {
        "user_input": message,
        "messages": [],
        "route": "",
        "plan": "",
        "research": "",
        "code": "",
        "review": "",
        "final_answer": "",
    }


def test_planner_route():
    result = graph.invoke(
        create_state("Create a roadmap for learning FastAPI")
    )

    assert result["route"] == "planner"
    assert "Supervisor selected: planner" in result["messages"]
    assert result["final_answer"]


def test_researcher_route():
    result = graph.invoke(
        create_state("What are the latest developments in AI?")
    )

    assert result["route"] == "researcher"
    assert "Supervisor selected: researcher" in result["messages"]
    assert result["final_answer"]


def test_coder_route():
    result = graph.invoke(
        create_state("Write a Python function to check prime numbers")
    )

    assert result["route"] == "coder"
    assert "Supervisor selected: coder" in result["messages"]
    assert "Coding completed." in result["messages"]
    assert "Reviewer finished." in result["messages"]
    assert result["final_answer"]


def test_reviewer_route():
    result = graph.invoke(
        create_state("Review this Python code for security problems")
    )

    assert result["route"] == "reviewer"
    assert "Supervisor selected: reviewer" in result["messages"]
    assert "Reviewer finished." in result["messages"]
    assert result["final_answer"]