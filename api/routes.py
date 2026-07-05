from fastapi import APIRouter, HTTPException

from api.schemas import ChatRequest, ChatResponse
from services.chat_service import chat_service


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    try:
        result = chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
        )

        return ChatResponse(**result)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )