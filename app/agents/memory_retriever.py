from app.state import AgentState
from database.memory import memory


class MemoryRetriever:

    def run(self, state: AgentState) -> AgentState:
        try:
            memories = memory.search(
                state["user_input"]
            )

            state["memories"] = memories

            state["messages"].append(
                f"Memory retrieved: {len(memories)} item(s)"
            )

        except Exception:
            state["memories"] = []

            state["messages"].append(
                "Memory retrieval unavailable."
            )

        return state


memory_retriever = MemoryRetriever()