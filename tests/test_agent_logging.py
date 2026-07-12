from unittest.mock import Mock

import pytest

from app.agents.logging_utils import (
    log_agent_execution,
)


class SuccessfulAgent:

    @log_agent_execution("successful")
    def run(self, state):
        return state


class FailingAgent:

    @log_agent_execution("failing")
    def run(self, state):
        raise RuntimeError("secret prompt content")


def test_agent_completion_is_logged(caplog):
    caplog.set_level("INFO")

    agent = SuccessfulAgent()

    state = {
        "conversation_id": "conversation-123",
    }

    agent.run(state)

    assert any(
        "agent_completed" in record.getMessage()
        and "successful" in record.getMessage()
        and "conversation-123"
        in record.getMessage()
        for record in caplog.records
    )


def test_agent_failure_is_logged(caplog):
    caplog.set_level("ERROR")

    agent = FailingAgent()

    state = {
        "conversation_id": "conversation-123",
    }

    with pytest.raises(RuntimeError):
        agent.run(state)

    assert any(
        "agent_failed" in record.getMessage()
        and "failing" in record.getMessage()
        for record in caplog.records
    )


def test_agent_logs_do_not_include_state_content(
    caplog,
):
    caplog.set_level("INFO")

    agent = SuccessfulAgent()

    state = {
        "conversation_id": "conversation-123",
        "user_input": "SUPER-SECRET-USER-MESSAGE",
        "plan": "SUPER-SECRET-PLAN",
    }

    agent.run(state)

    assert all(
        "SUPER-SECRET" not in record.getMessage()
        for record in caplog.records
    )