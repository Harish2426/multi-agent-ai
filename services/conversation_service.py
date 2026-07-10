import uuid

from database.repositories.conversation_repository import (
    ConversationRepository,
)
from database.repositories.message_repository import (
    MessageRepository,
)


class ConversationService:

    def __init__(self):
        self.conversations = ConversationRepository()
        self.messages = MessageRepository()

    def create(
        self,
        title: str | None = None,
        user_id: str | None = None,
    ):
        conversation_id = str(uuid.uuid4())

        if not title:
            title = "New Conversation"

        return self.conversations.create_conversation(
            conversation_id,
            title,
            user_id=user_id,
        )

    def add_user_message(
        self,
        conversation_id: str,
        content: str,
    ):
        return self.messages.add_message(
            conversation_id,
            "user",
            content,
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        content: str,
        route: str | None = None,
    ):
        return self.messages.add_message(
            conversation_id,
            "assistant",
            content,
            route,
        )

    def history(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ):
        if user_id is not None:
            conversation = (
                self.conversations.get_conversation(
                    conversation_id,
                    user_id=user_id,
                )
            )

            if conversation is None:
                return []

        return self.messages.get_messages(
            conversation_id
        )

    def get_history(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ):
        return self.history(
            conversation_id,
            user_id=user_id,
        )

    def list_conversations(
        self,
        user_id: str | None = None,
    ):
        return self.conversations.list_conversations(
            user_id=user_id
        )

    def delete(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ):
        if user_id is not None:
            conversation = (
                self.conversations.get_conversation(
                    conversation_id,
                    user_id=user_id,
                )
            )

            if conversation is None:
                return False

        self.messages.delete_messages(
            conversation_id
        )

        return self.conversations.delete_conversation(
            conversation_id,
            user_id=user_id,
        )

    def delete_conversation(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ):
        return self.delete(
            conversation_id,
            user_id=user_id,
        )


conversation_service = ConversationService()