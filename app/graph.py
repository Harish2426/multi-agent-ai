from langgraph.graph import StateGraph, END

from app.state import AgentState

from app.agents.planner import planner
from app.agents.researcher import researcher
from app.agents.coder import coder
from app.agents.reviewer import reviewer
from app.agents.writer import writer

builder = StateGraph(AgentState)

builder.add_node("planner", planner.run)
builder.add_node("researcher", researcher.run)
builder.add_node("coder", coder.run)
builder.add_node("reviewer", reviewer.run)
builder.add_node("writer", writer.run)

builder.set_entry_point("planner")

builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "coder")
builder.add_edge("coder", "reviewer")
builder.add_edge("reviewer", "writer")
builder.add_edge("writer", END)

graph = builder.compile()