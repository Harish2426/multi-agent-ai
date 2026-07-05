from app.agents.planner import PlannerAgent
from app.supervisor import SupervisorAgent


class FakeModel:

    def __init__(
        self,
        response: str,
    ):
        self.response = response
        self.prompts = []

    def generate(
        self,
        prompt: str,
        model_name: str | None = None,
    ) -> str:
        self.prompts.append(prompt)
        return self.response


def create_state(
    message: str,
) -> dict:
    return {
        "user_input": message,
        "conversation_id": "test-conversation",
        "messages": [],
        "route": "",
        "plan": "",
        "research": "",
        "code": "",
        "review": "",
        "tool_result": "",
        "memories": [],
        "final_answer": "",
    }


def test_planner_uses_injected_model():
    fake_model = FakeModel(
        "Injected planning response"
    )

    agent = PlannerAgent(
        model=fake_model
    )

    result = agent.run(
        create_state("Create a roadmap")
    )

    assert (
        result["plan"]
        == "Injected planning response"
    )

    assert len(fake_model.prompts) == 1


def test_supervisor_uses_injected_model():
    fake_model = FakeModel("coder")

    agent = SupervisorAgent(
        model=fake_model
    )

    route = agent.llm_route(
        "Do something ambiguous"
    )

    assert route == "coder"
    assert len(fake_model.prompts) == 1


def test_deterministic_route_does_not_call_model():
    fake_model = FakeModel("planner")

    agent = SupervisorAgent(
        model=fake_model
    )

    route = agent.deterministic_route(
        "45 * 78"
    )

    assert route == "calculator"
    assert fake_model.prompts == []