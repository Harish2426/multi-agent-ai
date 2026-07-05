from fastapi import APIRouter, HTTPException

from api.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    DeleteConversationResponse,
)

from services.chat_service import chat_service
from services.memory_service import memory_service


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    try:
        result = chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
        )

        return ChatResponse(**result)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Chat request failed.",
        )


@router.get(
    "/conversations/{conversation_id}/history",
    response_model=ConversationHistoryResponse,
)
def get_conversation_history(
    conversation_id: str,
):
    try:
        history = memory_service.get_history(
            conversation_id=conversation_id
        )

        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            history=history,
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve conversation history.",
        )


@router.delete(
    "/conversations/{conversation_id}",
    response_model=DeleteConversationResponse,
)
def delete_conversation(
    conversation_id: str,
):
    try:
        deleted_count = (
            memory_service.delete_conversation(
                conversation_id=conversation_id
            )
        )

        return DeleteConversationResponse(
            conversation_id=conversation_id,
            deleted_count=deleted_count,
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to delete conversation.",
        )