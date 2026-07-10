from datetime import datetime

from sqlalchemy.orm import Session

from database.sqlite import (
    Conversation,
    SessionLocal,
)


class ConversationRepository:

    def __init__(self):
        self.session: Session = SessionLocal()

    def create_conversation(
        self,
        conversation_id: str,
        title: str,
        user_id: str | None = None,
    ) -> Conversation:

        conversation = Conversation(
            id=conversation_id,
            title=title,
            user_id=user_id,
        )

        try:
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)

            return conversation

        except Exception:
            self.session.rollback()
            raise

    def get_conversation(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ) -> Conversation | None:

        query = self.session.query(
            Conversation
        ).filter(
            Conversation.id == conversation_id
        )

        if user_id is not None:
            query = query.filter(
                Conversation.user_id == user_id
            )

        return query.first()

    def list_conversations(
        self,
        user_id: str | None = None,
    ):

        query = self.session.query(Conversation)

        if user_id is not None:
            query = query.filter(
                Conversation.user_id == user_id
            )

        return query.order_by(
            Conversation.updated_at.desc()
        ).all()

    def update_title(
        self,
        conversation_id: str,
        title: str,
        user_id: str | None = None,
    ) -> Conversation | None:

        conversation = self.get_conversation(
            conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            return None

        conversation.title = title
        conversation.updated_at = datetime.utcnow()

        try:
            self.session.commit()
            self.session.refresh(conversation)

            return conversation

        except Exception:
            self.session.rollback()
            raise

    def delete_conversation(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ) -> bool:

        conversation = self.get_conversation(
            conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            return False

        try:
            self.session.delete(conversation)
            self.session.commit()

            return True

        except Exception:
            self.session.rollback()
            raise

    def close(self):
        self.session.close()


conversation_repository = ConversationRepository()