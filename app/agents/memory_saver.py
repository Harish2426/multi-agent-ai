from app.state import AgentState
from database.memory import memory


class MemorySaver:

    def run(self, state: AgentState) -> AgentState:
        try:
            final_answer = state.get("final_answer", "").strip()
            route = state.get("route", "")

            if final_answer and route != "calculator":
                memory.add(
                    user_input=state["user_input"],
                    assistant_response=final_answer,
                )

                state["messages"].append(
                    "Conversation saved to memory."
                )

        except Exception:
            state["messages"].append(
                "Memory save unavailable."
            )

        return state


memory_saver = MemorySaver()