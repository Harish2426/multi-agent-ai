from app.agents.logging_utils import (
    log_agent_execution,
)
from app.state import AgentState
from database.memory import memory


class MemoryRetriever:

    @log_agent_execution("memory_retriever")
    def run(
        self,
        state: AgentState,
    ) -> AgentState:

        try:
            memories = memory.search(
                conversation_id=state["conversation_id"],
                query=state["user_input"],
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