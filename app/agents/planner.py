from app.dependencies import get_model_client
from app.models import ModelClient
from app.state import AgentState
from app.prompts.planner_prompt import PLANNER_PROMPT


class PlannerAgent:

    def __init__(
        self,
        model: ModelClient | None = None,
    ):
        self.model = model

    def get_model(self) -> ModelClient:
        return self.model or get_model_client()

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