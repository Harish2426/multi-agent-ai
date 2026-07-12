import logging
import re

from app.dependencies import get_model_client
from app.models import ModelClient
from app.state import AgentState


logger = logging.getLogger(__name__)


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
        user_input: str,
    ) -> str | None:

        normalized_input = user_input.lower().strip()

        arithmetic_pattern = re.compile(
            r"^[\d\s\+\-\*\/\(\)\.\%]+$"
        )

        if arithmetic_pattern.fullmatch(
            normalized_input
        ):
            return "calculator"

        if any(
            keyword in normalized_input
            for keyword in [
                "calculate",
                "calculator",
                "what is the result of",
            ]
        ):
            return "calculator"

        if any(
            keyword in normalized_input
            for keyword in [
                "review this code",
                "review this python code",
                "code review",
                "review code",
                "security problems",
                "security issues",
                "check this code",
            ]
        ):
            return "reviewer"

        if any(
            keyword in normalized_input
            for keyword in [
                "write code",
                "write a python",
                "write python",
                "generate code",
                "implement",
                "create function",
                "create a function",
                "python function",
            ]
        ):
            return "coder"

        if any(
            keyword in normalized_input
            for keyword in [
                "research",
                "latest developments",
                "latest information",
                "find information",
                "investigate",
                "what are the latest",
            ]
        ):
            return "researcher"

        if any(
            keyword in normalized_input
            for keyword in [
                "plan",
                "roadmap",
                "strategy",
                "steps",
                "learning path",
            ]
        ):
            return "planner"

        return None

    def normalize_route(
        self,
        route: str,
    ) -> str:

        normalized_route = route.strip().lower()

        valid_routes = {
            "planner",
            "researcher",
            "coder",
            "reviewer",
            "calculator",
        }

        if normalized_route in valid_routes:
            return normalized_route

        return "planner"

    def llm_route(
        self,
        user_input: str,
    ) -> str:

        prompt = (
            "Route the following user request to exactly "
            "one of these routes: planner, researcher, "
            "coder, reviewer, calculator.\n\n"
            "Return only the route name.\n\n"
            "User request:\n"
            f"{user_input}"
        )

        model_route = self.get_model().generate(
            prompt
        )

        return self.normalize_route(
            model_route
        )

    def run(
        self,
        state: AgentState,
    ) -> AgentState:

        route = self.deterministic_route(
            state["user_input"]
        )

        # Deterministic routes bypass the model.
        if route is None:
            route = self.llm_route(
                state["user_input"]
            )

        state["route"] = route

        logger.info(
            "route_selected "
            "conversation_id=%s route=%s",
            state.get("conversation_id"),
            route,
        )

        state["messages"].append(
            f"Supervisor selected route: {route}"
        )

        return state


supervisor = SupervisorAgent()