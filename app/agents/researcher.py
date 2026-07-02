from app.models import gemini
from app.state import AgentState

from app.prompts.research_prompt import RESEARCH_PROMPT

from tools.search import search_tool


class ResearchAgent:

    def run(self, state: AgentState):

        results = search_tool.search(state["user_input"])
        print(results)
        prompt = RESEARCH_PROMPT.format(
            question=state["user_input"],
            search_results=results
        )

        research = gemini.generate(prompt)

        state["research"] = research

        state["messages"].append(
            "Research completed."
        )

        return state


researcher = ResearchAgent()