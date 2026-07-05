from app.models import ModelClient, gemini


def get_model_client() -> ModelClient:
    return gemini