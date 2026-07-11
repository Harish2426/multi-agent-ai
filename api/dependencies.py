from fastapi import Depends
from sqlalchemy.orm import Session

from database.repositories.user_repository import (
    UserRepository,
)
from database.session import get_database_session
from services.auth_service import AuthService
from services.chat_service import ChatService
from services.conversation_service import (
    ConversationService,
)


def get_user_repository(
    session: Session = Depends(
        get_database_session
    ),
) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(
    users: UserRepository = Depends(
        get_user_repository
    ),
) -> AuthService:
    return AuthService(
        user_repository_instance=users
    )


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