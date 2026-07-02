from app.models import gemini
from app.state import AgentState
from app.prompts.coding_prompt import CODING_PROMPT


class CodingAgent:

    def run(self, state: AgentState):

        prompt = CODING_PROMPT.format(
            question=state["user_input"],
            plan=state["plan"],
            research=state["research"]
        )

        code = gemini.generate(prompt)

        state["code"] = code

        state["messages"].append(
            "Coding completed."
        )

        return state


coder = CodingAgent()