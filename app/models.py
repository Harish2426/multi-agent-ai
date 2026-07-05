import time

from google import genai
from google.genai import errors

from app.config import GEMINI_API_KEY, MODEL_NAME


class ModelError(Exception):
    """Base exception for model failures."""


class ModelQuotaError(ModelError):
    """Raised when Gemini quota or rate limits are exhausted."""


class ModelUnavailableError(ModelError):
    """Raised when Gemini remains unavailable after retries."""


class ModelAuthenticationError(ModelError):
    """Raised when the Gemini API key is invalid or unauthorized."""


class ModelResponseError(ModelError):
    """Raised when Gemini returns an empty or unusable response."""


class GeminiClient:

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        max_retries: int = 2,
        retry_delay: float = 2.0,
    ):
        resolved_api_key = api_key or GEMINI_API_KEY

        if not resolved_api_key:
            raise ModelAuthenticationError(
                "GEMINI_API_KEY is missing."
            )

        self.client = genai.Client(
            api_key=resolved_api_key
        )

        self.model_name = (
            model_name
            or MODEL_NAME
            or "gemini-2.0-flash"
        )

        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def generate(
        self,
        prompt: str,
        model_name: str | None = None,
    ) -> str:

        selected_model = (
            model_name
            or self.model_name
        )

        for attempt in range(
            self.max_retries + 1
        ):
            try:
                response = (
                    self.client.models.generate_content(
                        model=selected_model,
                        contents=prompt,
                    )
                )

                text = response.text

                if not text or not text.strip():
                    raise ModelResponseError(
                        "Gemini returned an empty response."
                    )

                return text.strip()

            except errors.ClientError as error:
                status_code = getattr(
                    error,
                    "code",
                    None,
                )

                if status_code == 429:
                    raise ModelQuotaError(
                        "Gemini quota is exhausted or "
                        "the rate limit was exceeded."
                    ) from error

                if status_code in (401, 403):
                    raise ModelAuthenticationError(
                        "Gemini authentication failed. "
                        "Check your API key."
                    ) from error

                raise ModelError(
                    f"Gemini client error: {error}"
                ) from error

            except errors.ServerError as error:
                status_code = getattr(
                    error,
                    "code",
                    None,
                )

                if (
                    status_code == 503
                    and attempt < self.max_retries
                ):
                    delay = (
                        self.retry_delay
                        * (2 ** attempt)
                    )

                    time.sleep(delay)
                    continue

                if status_code == 503:
                    raise ModelUnavailableError(
                        "Gemini is temporarily unavailable "
                        "after retry attempts."
                    ) from error

                raise ModelError(
                    f"Gemini server error: {error}"
                ) from error

            except ModelError:
                raise

            except Exception as error:
                raise ModelError(
                    f"Unexpected Gemini error: {error}"
                ) from error

        raise ModelUnavailableError(
            "Gemini request failed."
        )


gemini = GeminiClient()