from fastapi import Depends
from sqlalchemy.orm import Session

from database.session import get_database_session
from services.chat_service import ChatService
from services.conversation_service import ConversationService


def get_conversation_service(
    session: Session = Depends(
        get_database_session
    ),
) -> ConversationService:
    return ConversationService(
        session=session
    )


def get_chat_service(
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
) -> ChatService:
    return ChatService(
        conversation_service=conversation_service
    )