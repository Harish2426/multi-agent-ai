from app.agents.logging_utils import (
    log_agent_execution,
)
from app.dependencies import get_model_client
from app.models import ModelClient
from app.prompts.coding_prompt import CODING_PROMPT
from app.state import AgentState


class CoderAgent:

    def __init__(
        self,
        model: ModelClient | None = None,
    ):
        self.model = model

    def get_model(self) -> ModelClient:
        return self.model or get_model_client()

    @log_agent_execution("coder")
    def run(
        self,
        state: AgentState,
    ) -> AgentState:
        prompt = CODING_PROMPT.format(
            question=state["user_input"],
            plan=state["plan"],
            research=state["research"],
        )

        state["code"] = self.get_model().generate(
            prompt
        )

        state["messages"].append(
            "Coding completed."
        )

        return state


coder = CoderAgent()