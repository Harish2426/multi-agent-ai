from app.agents.logging_utils import (
    log_agent_execution,
)
from app.dependencies import get_model_client
from app.models import ModelClient
from app.prompts.writer_prompt import WRITER_PROMPT
from app.state import AgentState


class WriterAgent:

    def __init__(
        self,
        model: ModelClient | None = None,
    ):
        self.model = model

    def get_model(self) -> ModelClient:
        return self.model or get_model_client()

    @log_agent_execution("writer")
    def run(
        self,
        state: AgentState,
    ) -> AgentState:

        memories = state.get(
            "memories",
            [],
        )

        memory_context = (
            "\n\n".join(memories)
            if memories
            else "No relevant previous conversations."
        )

        prompt = WRITER_PROMPT.format(
            question=state["user_input"],
            memories=memory_context,
            plan=state["plan"],
            research=state["research"],
            code=state["code"],
            review=state["review"],
        )

        state["final_answer"] = (
            self.get_model().generate(prompt)
        )

        state["messages"].append(
            "Writer completed."
        )

        return state


writer = WriterAgent()