from app.models import (
    ModelAuthenticationError,
    ModelError,
    ModelQuotaError,
    ModelResponseError,
    ModelUnavailableError,
)


def model_error_message(error: Exception) -> str:

    if isinstance(error, ModelQuotaError):
        return (
            "The AI model quota is currently exhausted. "
            "Please try again later or check the API plan."
        )

    if isinstance(error, ModelUnavailableError):
        return (
            "The AI model is temporarily unavailable. "
            "Please try again shortly."
        )

    if isinstance(error, ModelAuthenticationError):
        return (
            "The AI model configuration is invalid. "
            "Check the Gemini API key."
        )

    if isinstance(error, ModelResponseError):
        return (
            "The AI model returned an empty response."
        )

    if isinstance(error, ModelError):
        return (
            "The AI model request failed."
        )

    return "An unexpected server error occurred."