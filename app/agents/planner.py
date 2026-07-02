from app.models import gemini
from app.state import AgentState
from app.prompts.planner_prompt import PLANNER_PROMPT


class PlannerAgent:

    def run(self, state: AgentState):

        prompt = PLANNER_PROMPT.format(
            question=state["user_input"]
        )

        plan = gemini.generate(prompt)

        state["plan"] = plan

        state["messages"].append(
            "Planner finished."
        )

        return state


planner = PlannerAgent()