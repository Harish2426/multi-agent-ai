from app.models import gemini
from app.state import AgentState
from app.prompts.review_prompt import REVIEW_PROMPT


class ReviewerAgent:

    def run(self, state: AgentState):

        prompt = REVIEW_PROMPT.format(
            question=state["user_input"],
            plan=state["plan"],
            research=state["research"],
            code=state["code"]
        )

        review = gemini.generate(prompt)

        state["review"] = review

        state["messages"].append(
            "Reviewer finished."
        )

        return state


reviewer = ReviewerAgent()