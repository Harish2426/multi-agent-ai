from app.agents.logging_utils import (
    log_agent_execution,
)
from app.dependencies import get_model_client
from app.models import ModelClient
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.state import AgentState


class PlannerAgent:

    def __init__(
        self,
        model: ModelClient | None = None,
    ):
        self.model = model

    def get_model(self) -> ModelClient:
        return self.model or get_model_client()

    @log_agent_execution("planner")
    def run(
        self,
        state: AgentState,
    ) -> AgentState:
        prompt = PLANNER_PROMPT.format(
            question=state["user_input"]
        )

        state["plan"] = self.get_model().generate(
            prompt
        )

        state["messages"].append(
            "Planner finished."
        )

        return state


planner = PlannerAgent()