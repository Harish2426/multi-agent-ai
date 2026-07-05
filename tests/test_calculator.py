import pytest

from tools.calculator import calculator_tool
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
        "tool_result": "",
        "final_answer": "",
    }


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("45 + 45", 90),
        ("10 * 5", 50),
        ("100 / 4", 25),
        ("2 ** 8", 256),
        ("(10 + 5) * 2", 30),
    ],
)
def test_calculator_tool(expression, expected):
    result = calculator_tool.calculate(expression)
    assert result == expected


def test_calculator_rejects_code():
    with pytest.raises(ValueError):
        calculator_tool.calculate(
            "__import__('os').system('dir')"
        )


def test_graph_routes_math_to_calculator():
    result = graph.invoke(
        create_state("45 * 78")
    )

    assert result["route"] == "calculator"
    assert result["tool_result"] == "3510"
    assert result["final_answer"] == "3510"
    assert "Calculator completed." in result["messages"]