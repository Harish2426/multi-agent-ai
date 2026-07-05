from app.supervisor import supervisor


def test_planner_route():
    assert (
        supervisor.deterministic_route(
            "Create a roadmap for learning FastAPI"
        )
        == "planner"
    )


def test_researcher_route():
    assert (
        supervisor.deterministic_route(
            "What are the latest developments in AI?"
        )
        == "researcher"
    )


def test_coder_route():
    assert (
        supervisor.deterministic_route(
            "Write a Python function to check prime numbers"
        )
        == "coder"
    )


def test_reviewer_route():
    assert (
        supervisor.deterministic_route(
            "Review this Python code for security problems"
        )
        == "reviewer"
    )


def test_calculator_route():
    assert (
        supervisor.deterministic_route("45 * 78")
        == "calculator"
    )


def test_ambiguous_route():
    assert (
        supervisor.deterministic_route(
            "Tell me something interesting"
        )
        is None
    )