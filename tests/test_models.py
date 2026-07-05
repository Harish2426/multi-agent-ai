from unittest.mock import Mock, patch

import pytest

from google.genai import errors

from app.models import (
    GeminiClient,
    ModelQuotaError,
    ModelResponseError,
)


def create_client():
    client = GeminiClient(
        api_key="fake-test-key",
        model_name="test-model",
        max_retries=0,
        retry_delay=0,
    )

    client.client = Mock()

    return client


def test_generate_returns_text():
    client = create_client()

    response = Mock()
    response.text = "Hello from Gemini"

    client.client.models.generate_content.return_value = (
        response
    )

    result = client.generate("Hello")

    assert result == "Hello from Gemini"


def test_empty_response_raises_error():
    client = create_client()

    response = Mock()
    response.text = ""

    client.client.models.generate_content.return_value = (
        response
    )

    with pytest.raises(ModelResponseError):
        client.generate("Hello")


def test_unexpected_error_becomes_model_error():
    from app.models import ModelError

    client = create_client()

    client.client.models.generate_content.side_effect = (
        RuntimeError("network failure")
    )

    with pytest.raises(ModelError):
        client.generate("Hello")