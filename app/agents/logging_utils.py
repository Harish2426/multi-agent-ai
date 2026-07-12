import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


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

            # Normal agent method:
            # run(self, state)
            if len(args) >= 2:
                state = args[1]

            # Support state passed by keyword.
            elif "state" in kwargs:
                state = kwargs["state"]

            conversation_id = None

            if isinstance(state, dict):
                conversation_id = state.get(
                    "conversation_id"
                )

            logger.info(
                "agent_started "
                "agent=%s conversation_id=%s",
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

                logger.exception(
                    "agent_failed "
                    "agent=%s conversation_id=%s "
                    "duration_ms=%.2f",
                    agent_name,
                    conversation_id,
                    duration_ms,
                )

                raise

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            logger.info(
                "agent_completed "
                "agent=%s conversation_id=%s "
                "duration_ms=%.2f",
                agent_name,
                conversation_id,
                duration_ms,
            )

            return result

        return wrapper

    return decorator