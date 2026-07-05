import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.models import (
    ModelAuthenticationError,
    ModelError,
    ModelQuotaError,
    ModelUnavailableError,
)


logger = logging.getLogger(__name__)


async def model_error_handler(
    request: Request,
    error: ModelError,
):
    if isinstance(error, ModelQuotaError):
        status_code = 503
        message = "AI model quota is unavailable."

    elif isinstance(error, ModelUnavailableError):
        status_code = 503
        message = "AI model is temporarily unavailable."

    elif isinstance(error, ModelAuthenticationError):
        status_code = 503
        message = "AI model configuration is unavailable."

    else:
        status_code = 502
        message = "AI model request failed."

    logger.warning(
        "Model error on %s: %s",
        request.url.path,
        type(error).__name__,
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "detail": message,
        },
    )


async def unexpected_error_handler(
    request: Request,
    error: Exception,
):
    logger.exception(
        "Unhandled error on %s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
        },
    )