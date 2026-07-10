from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.routes.auth_routes import get_current_user
from services.conversation_service import conversation_service


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


class RenameConversationRequest(BaseModel):
    title: str


def serialize_message(message):
    if isinstance(message, dict):
        return {
            "id": message.get("id"),
            "role": message.get("role"),
            "content": message.get("content"),
            "route": message.get("route"),
            "created_at": message.get(
                "created_at",
                message.get("timestamp"),
            ),
            "sequence": message.get("sequence"),
        }

    return {
        "id": getattr(message, "id", None),
        "role": getattr(message, "role", None),
        "content": getattr(message, "content", None),
        "route": getattr(message, "route", None),
        "created_at": getattr(
            message,
            "created_at",
            None,
        ),
        "sequence": getattr(
            message,
            "sequence",
            None,
        ),
    }


@router.get("")
def list_conversations(
    current_user=Depends(get_current_user),
):
    conversations = (
        conversation_service.list_conversations(
            user_id=current_user.id,
        )
    )

    return [
        {
            "id": conversation.id,
            "title": conversation.title,
            "updated_at": conversation.updated_at,
        }
        for conversation in conversations
    ]


@router.get("/{conversation_id}/history")
def get_history_legacy(
    conversation_id: str,
    current_user=Depends(get_current_user),
):
    history = conversation_service.get_history(
        conversation_id,
        user_id=current_user.id,
    )

    return {
        "conversation_id": conversation_id,
        "history": [
            serialize_message(message)
            for message in history
        ],
    }


@router.get("/{conversation_id}")
def get_history(
    conversation_id: str,
    current_user=Depends(get_current_user),
):
    history = conversation_service.get_history(
        conversation_id,
        user_id=current_user.id,
    )

    return {
        "conversation_id": conversation_id,
        "history": [
            serialize_message(message)
            for message in history
        ],
    }


@router.patch("/{conversation_id}")
def rename(
    conversation_id: str,
    request: RenameConversationRequest,
    current_user=Depends(get_current_user),
):
    conversation = (
        conversation_service.conversations.update_title(
            conversation_id,
            request.title,
            user_id=current_user.id,
        )
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "id": conversation.id,
        "title": conversation.title,
    }


@router.delete("/{conversation_id}")
def delete(
    conversation_id: str,
    current_user=Depends(get_current_user),
):
    deleted = (
        conversation_service.delete_conversation(
            conversation_id,
            user_id=current_user.id,
        )
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "conversation_id": conversation_id,
        "deleted_count": (
            deleted
            if isinstance(deleted, int)
            and not isinstance(deleted, bool)
            else 1
        ),
    }