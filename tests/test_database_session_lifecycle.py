from database.sqlite import SessionLocal
from database.repositories.conversation_repository import (
    ConversationRepository,
)
from database.repositories.message_repository import (
    MessageRepository,
)
from services.conversation_service import (
    ConversationService,
)


def test_conversation_repository_accepts_session():
    session = SessionLocal()

    try:
        repository = ConversationRepository(
            session=session
        )

        assert repository.session is session
        assert repository._owns_session is False

    finally:
        session.close()


def test_message_repository_accepts_session():
    session = SessionLocal()

    try:
        repository = MessageRepository(
            session=session
        )

        assert repository.session is session
        assert repository._owns_session is False

    finally:
        session.close()


def test_service_shares_injected_session():
    session = SessionLocal()

    try:
        service = ConversationService(
            session=session
        )

        assert service.conversations.session is session
        assert service.messages.session is session

    finally:
        session.close()