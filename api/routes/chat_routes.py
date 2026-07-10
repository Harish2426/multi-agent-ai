from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from pydantic import BaseModel, field_validator

from api.routes.auth_routes import get_current_user
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
        value = value.strip()

        if not value:
            raise ValueError(
                "Message cannot be empty."
            )

        return value


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
    try:
        return chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
        )

    except PermissionError:
        # Do not reveal whether a conversation belongs
        # to another user or does not exist.
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
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
    return {
        "status": "ready",
        "database": "available",
    }