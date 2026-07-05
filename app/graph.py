from langgraph.graph import StateGraph, START, END

from app.state import AgentState
from app.supervisor import supervisor

from app.agents.memory_retriever import memory_retriever
from app.agents.memory_saver import memory_saver

from app.agents.planner import planner
from app.agents.researcher import researcher
from app.agents.coder import coder
from app.agents.reviewer import reviewer
from app.agents.writer import writer
from app.agents.calculator_agent import calculator_agent


def select_route(state: AgentState) -> str:
    return state["route"]


builder = StateGraph(AgentState)

builder.add_node(
    "supervisor",
    supervisor.run,
)

builder.add_node(
    "memory_retriever",
    memory_retriever.run,
)

builder.add_node(
    "planner",
    planner.run,
)

builder.add_node(
    "researcher",
    researcher.run,
)

builder.add_node(
    "coder",
    coder.run,
)

builder.add_node(
    "reviewer",
    reviewer.run,
)

builder.add_node(
    "writer",
    writer.run,
)

builder.add_node(
    "calculator",
    calculator_agent.run,
)

builder.add_node(
    "memory_saver",
    memory_saver.run,
)


# Entry point

builder.add_edge(
    START,
    "supervisor",
)


# Dynamic routing

builder.add_conditional_edges(
    "supervisor",
    select_route,
    {
        "planner": "memory_retriever",
        "researcher": "memory_retriever",
        "coder": "memory_retriever",
        "reviewer": "memory_retriever",
        "calculator": "calculator",
    },
)


# Route after memory retrieval.

def route_after_memory(
    state: AgentState,
) -> str:
    return state["route"]


builder.add_conditional_edges(
    "memory_retriever",
    route_after_memory,
    {
        "planner": "planner",
        "researcher": "researcher",
        "coder": "coder",
        "reviewer": "reviewer",
    },
)


builder.add_edge(
    "planner",
    "writer",
)

builder.add_edge(
    "researcher",
    "writer",
)

builder.add_edge(
    "coder",
    "reviewer",
)

builder.add_edge(
    "reviewer",
    "writer",
)

builder.add_edge(
    "writer",
    "memory_saver",
)

builder.add_edge(
    "memory_saver",
    END,
)


# Calculator bypasses both Gemini and memory.

builder.add_edge(
    "calculator",
    END,
)


graph = builder.compile()