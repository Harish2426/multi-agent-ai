from app.dependencies import get_model_client
from app.models import ModelClient
from app.state import AgentState

from app.prompts.research_prompt import RESEARCH_PROMPT
from tools.search import search_tool


class ResearchAgent:

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

        results = search_tool.search(
            state["user_input"]
        )

        prompt = RESEARCH_PROMPT.format(
            question=state["user_input"],
            search_results=results,
        )

        research = self.get_model().generate(
            prompt
        )

        state["research"] = research

        state["messages"].append(
            "Research completed."
        )

        return state


researcher = ResearchAgent()