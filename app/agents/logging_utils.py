import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from app.logging_context import get_request_id
from app.metrics import AGENT_DURATION


def log_agent_execution(
    agent_name: str,
):
    def decorator(
        function: Callable[..., Any],
    ):
        @wraps(function)
        def wrapper(*args, **kwargs):

            logger = logging.getLogger(
                function.__module__
            )

            started_at = time.perf_counter()

            state = None

            if len(args) >= 2:
                state = args[1]

            elif "state" in kwargs:
                state = kwargs["state"]

            conversation_id = None

            if isinstance(state, dict):
                conversation_id = state.get(
                    "conversation_id"
                )

            request_id = get_request_id()

            logger.info(
                "agent_started "
                "request_id=%s "
                "agent=%s "
                "conversation_id=%s",
                request_id,
                agent_name,
                conversation_id,
            )

            try:

                result = function(
                    *args,
                    **kwargs,
                )

            except Exception:

                duration_ms = (
                    time.perf_counter()
                    - started_at
                ) * 1000

                AGENT_DURATION.labels(
                    agent_name
                ).observe(
                    duration_ms / 1000
                )

                logger.exception(
                    "agent_failed "
                    "request_id=%s "
                    "agent=%s "
                    "conversation_id=%s "
                    "duration_ms=%.2f",
                    request_id,
                    agent_name,
                    conversation_id,
                    duration_ms,
                )

                raise

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            AGENT_DURATION.labels(
                agent_name
            ).observe(
                duration_ms / 1000
            )

            logger.info(
                "agent_completed "
                "request_id=%s "
                "agent=%s "
                "conversation_id=%s "
                "duration_ms=%.2f",
                request_id,
                agent_name,
                conversation_id,
                duration_ms,
            )

            return result

        return wrapper

    return decorator