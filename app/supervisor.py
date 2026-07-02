from app.models import gemini
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT


class Supervisor:

    def route(self, question):

        prompt = SUPERVISOR_PROMPT.format(
            question=question
        )

        decision = gemini.generate(prompt)

        decision = decision.lower().strip()

        if "planner" in decision:
            return "planner"

        elif "research" in decision:
            return "researcher"

        elif "coder" in decision:
            return "coder"

        elif "review" in decision:
            return "reviewer"

        return "planner"


supervisor = Supervisor()