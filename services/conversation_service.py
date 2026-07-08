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
    ):
        conversation_id = str(uuid.uuid4())

        if not title:
            title = "New Conversation"

        return self.conversations.create_conversation(
            conversation_id,
            title,
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
    ):
        return self.messages.get_messages(
            conversation_id
        )

    # ------------------------------------------------------------------
    # Compatibility methods for older tests
    # ------------------------------------------------------------------

    def get_history(
        self,
        conversation_id: str,
    ):
        return self.history(
            conversation_id
        )

    def list_conversations(
        self,
    ):
        return self.conversations.list_conversations()

    def delete(
        self,
        conversation_id: str,
    ):
        self.messages.delete_messages(
            conversation_id
        )

        return self.conversations.delete_conversation(
            conversation_id
        )

    def delete_conversation(
        self,
        conversation_id: str,
    ):
        return self.delete(
            conversation_id
        )


conversation_service = ConversationService()