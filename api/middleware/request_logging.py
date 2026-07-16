import logging
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logging_context import (
    reset_request_id,
    set_request_id,
)
from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
)

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        request_id = (
            request.headers.get("X-Request-ID")
            or str(uuid4())
        )

        request.state.request_id = request_id

        token = set_request_id(request_id)

        started_at = time.perf_counter()

        logger.info(
            "request_started "
            "request_id=%s method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(request)

        except Exception:

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            REQUEST_COUNT.labels(
                request.method,
                request.url.path,
                500,
            ).inc()

            REQUEST_LATENCY.labels(
                request.method,
                request.url.path,
            ).observe(
                duration_ms / 1000
            )

            logger.exception(
                "request_failed "
                "request_id=%s "
                "method=%s "
                "path=%s "
                "duration_ms=%.2f",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )

            raise

        duration_ms = (
            time.perf_counter()
            - started_at
        ) * 1000

        REQUEST_COUNT.labels(
            request.method,
            request.url.path,
            response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            request.method,
            request.url.path,
        ).observe(
            duration_ms / 1000
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        logger.info(
            "request_completed "
            "request_id=%s "
            "method=%s "
            "path=%s "
            "status_code=%s "
            "duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        reset_request_id(token)

        return response