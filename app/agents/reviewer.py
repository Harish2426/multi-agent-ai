from app.agents.logging_utils import (
    log_agent_execution,
)
from app.dependencies import get_model_client
from app.models import ModelClient
from app.prompts.review_prompt import REVIEW_PROMPT
from app.state import AgentState


class ReviewerAgent:

    def __init__(
        self,
        model: ModelClient | None = None,
    ):
        self.model = model

    def get_model(self) -> ModelClient:
        return self.model or get_model_client()

    @log_agent_execution("reviewer")
    def run(
        self,
        state: AgentState,
    ) -> AgentState:
        prompt = REVIEW_PROMPT.format(
            question=state["user_input"],
            plan=state.get("plan", ""),
            research=state.get("research", ""),
            code=state.get("code", ""),
        )

        state["review"] = (
            self.get_model().generate(prompt)
        )

        state["messages"].append(
            "Review completed."
        )

        return state


reviewer = ReviewerAgent()