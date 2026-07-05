from fastapi import APIRouter

from api.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    DeleteConversationResponse,
    HealthResponse,
    ReadinessResponse,
)

from database.memory import memory
from services.chat_service import chat_service
from services.memory_service import memory_service


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return HealthResponse(
        status="ok"
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
)
def ready():
    memory.collection.count()

    return ReadinessResponse(
        status="ready",
        memory="available",
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    result = chat_service.chat(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(**result)


@router.get(
    "/conversations/{conversation_id}/history",
    response_model=ConversationHistoryResponse,
)
def get_conversation_history(
    conversation_id: str,
):
    history = memory_service.get_history(
        conversation_id=conversation_id
    )

    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        history=history,
    )


@router.delete(
    "/conversations/{conversation_id}",
    response_model=DeleteConversationResponse,
)
def delete_conversation(
    conversation_id: str,
):
    deleted_count = (
        memory_service.delete_conversation(
            conversation_id=conversation_id
        )
    )

    return DeleteConversationResponse(
        conversation_id=conversation_id,
        deleted_count=deleted_count,
    )