from langgraph.graph import StateGraph, START, END

from app.state import AgentState
from app.supervisor import supervisor

from app.agents.planner import planner
from app.agents.researcher import researcher
from app.agents.coder import coder
from app.agents.reviewer import reviewer
from app.agents.writer import writer
from app.agents.calculator_agent import calculator_agent


def select_route(state: AgentState) -> str:
    """
    Return the route selected by the Supervisor Agent.
    """

    return state["route"]


# --------------------------------------------------
# Create graph builder
# --------------------------------------------------

builder = StateGraph(AgentState)


# --------------------------------------------------
# Register nodes
# --------------------------------------------------

builder.add_node(
    "supervisor",
    supervisor.run,
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


# --------------------------------------------------
# Graph entry point
# --------------------------------------------------

builder.add_edge(
    START,
    "supervisor",
)


# --------------------------------------------------
# Dynamic routing
# --------------------------------------------------

builder.add_conditional_edges(
    "supervisor",
    select_route,
    {
        "planner": "planner",
        "researcher": "researcher",
        "coder": "coder",
        "reviewer": "reviewer",
        "calculator": "calculator",
    },
)


# --------------------------------------------------
# Planner workflow
#
# Supervisor
#     ↓
# Planner
#     ↓
# Writer
#     ↓
# END
# --------------------------------------------------

builder.add_edge(
    "planner",
    "writer",
)


# --------------------------------------------------
# Research workflow
#
# Supervisor
#     ↓
# Researcher
#     ↓
# Writer
#     ↓
# END
# --------------------------------------------------

builder.add_edge(
    "researcher",
    "writer",
)


# --------------------------------------------------
# Coding workflow
#
# Supervisor
#     ↓
# Coder
#     ↓
# Reviewer
#     ↓
# Writer
#     ↓
# END
# --------------------------------------------------

builder.add_edge(
    "coder",
    "reviewer",
)


# --------------------------------------------------
# Reviewer workflow
#
# Supervisor
#     ↓
# Reviewer
#     ↓
# Writer
#     ↓
# END
# --------------------------------------------------

builder.add_edge(
    "reviewer",
    "writer",
)


# --------------------------------------------------
# Writer finishes LLM workflows
# --------------------------------------------------

builder.add_edge(
    "writer",
    END,
)


# --------------------------------------------------
# Calculator workflow
#
# Supervisor
#     ↓
# Calculator
#     ↓
# END
#
# Calculator intentionally bypasses Writer/Gemini.
# --------------------------------------------------

builder.add_edge(
    "calculator",
    END,
)


# --------------------------------------------------
# Compile graph
# --------------------------------------------------

graph = builder.compile()