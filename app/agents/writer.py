from app.models import gemini
from app.state import AgentState
from app.prompts.writer_prompt import WRITER_PROMPT


class WriterAgent:

    def run(self, state: AgentState):

        prompt = WRITER_PROMPT.format(
            question=state["user_input"],
            plan=state["plan"],
            research=state["research"],
            code=state["code"],
            review=state["review"]
        )

        answer = gemini.generate(prompt)

        state["final_answer"] = answer

        state["messages"].append(
            "Writer completed."
        )

        return state


writer = WriterAgent()