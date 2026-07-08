from app.dependencies import get_model_client
from app.models import ModelClient
from app.state import AgentState
from app.prompts.review_prompt import REVIEW_PROMPT


class ReviewerAgent:

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

        prompt = REVIEW_PROMPT.format(
            question=state.get(
                "user_input",
                "",
            ),
            plan=state.get(
                "plan",
                "",
            ),
            research=state.get(
                "research",
                "",
            ),
            code=state.get(
                "code",
                "",
            ),
        )

        state["review"] = self.get_model().generate(
            prompt
        )

        state["final_answer"] = state["review"]

        state["messages"].append(
            "Review completed."
        )

        return state


reviewer = ReviewerAgent()