from app.agents.logging_utils import (
    log_agent_execution,
)
from app.state import AgentState
from tools.calculator import calculator_tool


class CalculatorAgent:

    @log_agent_execution("calculator")
    def run(
        self,
        state: AgentState,
    ) -> AgentState:
        try:
            result = calculator_tool.calculate(
                state["user_input"]
            )

            state["tool_result"] = str(result)
            state["final_answer"] = str(result)

            state["messages"].append(
                "Calculator completed."
            )

        except Exception as error:
            state["tool_result"] = ""
            state["final_answer"] = (
                f"Calculator error: {error}"
            )

            state["messages"].append(
                "Calculator failed."
            )

        return state


calculator_agent = CalculatorAgent()