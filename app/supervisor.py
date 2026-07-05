from app.dependencies import get_model_client
from app.models import ModelClient
from app.state import AgentState
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT


VALID_ROUTES = {
    "planner",
    "researcher",
    "coder",
    "reviewer",
    "calculator",
}


class SupervisorAgent:

    def __init__(
        self,
        model: ModelClient | None = None,
    ):
        self.model = model

    def get_model(self) -> ModelClient:
        return self.model or get_model_client()

    def deterministic_route(
        self,
        question: str,
    ) -> str | None:
        text = question.lower().strip()

        reviewer_words = (
            "review",
            "audit",
            "critique",
            "inspect code",
            "check code",
            "security problems",
            "security issues",
            "code quality",
        )

        coder_words = (
            "write code",
            "write a python",
            "create a function",
            "implement",
            "debug",
            "fix error",
            "fix bug",
            "refactor",
            "program",
            "build an api",
            "build a rest api",
        )

        researcher_words = (
            "latest",
            "current",
            "recent",
            "news",
            "research",
            "developments",
            "trends",
            "compare",
            "find information",
        )

        planner_words = (
            "plan",
            "roadmap",
            "architecture",
            "design",
            "strategy",
            "steps",
            "approach",
        )

        # Local calculator routing.
        # This keeps obvious arithmetic away from Gemini.
        calculator_words = (
            "calculate",
            "calculator",
            "compute",
            "evaluate",
        )

        if any(
            word in text
            for word in reviewer_words
        ):
            return "reviewer"

        if any(
            word in text
            for word in coder_words
        ):
            return "coder"

        if any(
            word in text
            for word in researcher_words
        ):
            return "researcher"

        if any(
            word in text
            for word in planner_words
        ):
            return "planner"

        if any(
            word in text
            for word in calculator_words
        ):
            return "calculator"

        # Preserve your existing arithmetic detection.
        arithmetic_characters = set(
            "0123456789+-*/().% "
        )

        if (
            text
            and any(character.isdigit() for character in text)
            and all(
                character in arithmetic_characters
                for character in text
            )
        ):
            return "calculator"

        return None

    def llm_route(
        self,
        question: str,
    ) -> str | None:
        prompt = SUPERVISOR_PROMPT.format(
            question=question
        )

        decision = self.get_model().generate(
            prompt
        )

        route = decision.strip().lower()

        for valid_route in VALID_ROUTES:
            if valid_route in route:
                return valid_route

        return None

    def run(
        self,
        state: AgentState,
    ) -> AgentState:
        question = state["user_input"]

        route = self.deterministic_route(
            question
        )

        routing_method = "deterministic"

        if route is None:
            route = self.llm_route(question)
            routing_method = "llm"

        if route not in VALID_ROUTES:
            route = "planner"
            routing_method = "fallback"

        state["route"] = route

        state["messages"].append(
            f"Supervisor selected: {route}"
        )

        state["messages"].append(
            f"Routing method: {routing_method}"
        )

        return state


supervisor = SupervisorAgent()