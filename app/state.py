from typing import TypedDict, List


class AgentState(TypedDict):

    user_input: str

    messages: List[str]

    plan: str

    research: str

    code: str

    review: str

    final_answer: str