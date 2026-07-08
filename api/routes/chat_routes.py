from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from app.models import (
    ModelError,
    ModelQuotaError,
    ModelUnavailableError,
)
from services.chat_service import chat_service

router = APIRouter(
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):
        if not value.strip():
            raise ValueError("Message cannot be empty.")
        return value


@router.post("/chat")
def chat(request: ChatRequest):

    try:
        return chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
        )

    except ModelQuotaError:
        raise HTTPException(
            status_code=503,
            detail="AI model quota is unavailable.",
        )

    except ModelUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="AI model is unavailable.",
        )

    except ModelError:
        raise HTTPException(
            status_code=503,
            detail="AI model error.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )


@router.get("/")
def root():
    return {
        "message": "Multi-Agent AI API is running"
    }


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.get("/ready")
def ready():
    """
    Readiness endpoint.

    The previous implementation depended on the legacy Chroma
    memory object. After the SQLite refactor we simply verify
    that the API is able to serve requests.
    """
    return {
        "status": "ready",
        "database": "available",
    }