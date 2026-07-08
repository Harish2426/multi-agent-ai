from sqlalchemy.orm import Session

from database.sqlite import (
    Message,
    SessionLocal,
)


class MessageRepository:

    def __init__(self):
        self.session: Session = SessionLocal()

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        route: str | None = None,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            route=route,
        )

        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        return message

    def get_messages(
        self,
        conversation_id: str,
    ):

        return (
            self.session.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.id.asc())
            .all()
        )

    def delete_messages(
        self,
        conversation_id: str,
    ) -> int:

        deleted = (
            self.session.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .delete()
        )

        self.session.commit()

        return deleted

    def close(self):
        self.session.close()


message_repository = MessageRepository()