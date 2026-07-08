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
    ) -> Conversation:

        conversation = Conversation(
            id=conversation_id,
            title=title,
        )

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def get_conversation(
        self,
        conversation_id: str,
    ) -> Conversation | None:

        return (
            self.session.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

    def list_conversations(self):

        return (
            self.session.query(Conversation)
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

    def update_title(
        self,
        conversation_id: str,
        title: str,
    ) -> Conversation | None:

        conversation = self.get_conversation(
            conversation_id
        )

        if conversation is None:
            return None

        conversation.title = title
        conversation.updated_at = datetime.utcnow()

        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> bool:

        conversation = self.get_conversation(
            conversation_id
        )

        if conversation is None:
            return False

        self.session.delete(conversation)
        self.session.commit()

        return True

    def close(self):
        self.session.close()


conversation_repository = ConversationRepository()