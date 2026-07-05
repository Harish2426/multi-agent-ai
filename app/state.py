from typing import TypedDict


class AgentState(TypedDict):
    user_input: str
    messages: list[str]

    route: str

    plan: str
    research: str
    code: str
    review: str

    tool_result: str

    final_answer: str