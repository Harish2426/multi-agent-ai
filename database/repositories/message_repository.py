from sqlalchemy.orm import Session

from database.sqlite import (
    Message,
    SessionLocal,
)


class MessageRepository:

    def __init__(
        self,
        session: Session | None = None,
    ):
        self.session = session or SessionLocal()
        self._owns_session = session is None

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

        try:
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)

            return message

        except Exception:
            self.session.rollback()
            raise

    def add_message_pair(
        self,
        conversation_id: str,
        user_content: str,
        assistant_content: str,
        route: str | None = None,
    ) -> tuple[Message, Message]:

        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_content,
        )

        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content,
            route=route,
        )

        try:
            self.session.add_all(
                [
                    user_message,
                    assistant_message,
                ]
            )

            self.session.flush()
            self.session.commit()

            self.session.refresh(user_message)
            self.session.refresh(
                assistant_message
            )

            return (
                user_message,
                assistant_message,
            )

        except Exception:
            self.session.rollback()
            raise

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[Message]:

        return (
            self.session.query(Message)
            .filter(
                Message.conversation_id
                == conversation_id
            )
            .order_by(Message.id.asc())
            .all()
        )

    def delete_messages(
        self,
        conversation_id: str,
    ) -> int:

        try:
            deleted = (
                self.session.query(Message)
                .filter(
                    Message.conversation_id
                    == conversation_id
                )
                .delete()
            )

            self.session.commit()

            return deleted

        except Exception:
            self.session.rollback()
            raise

    def close(self):
        if self._owns_session:
            self.session.close()


message_repository = MessageRepository()