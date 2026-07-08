import uuid

from database.repositories.message_repository import (
    MessageRepository,
)
from database.repositories.conversation_repository import (
    ConversationRepository,
)


def test_add_and_get_messages():

    conversation_repo = ConversationRepository()
    message_repo = MessageRepository()

    conversation_id = str(uuid.uuid4())

    conversation_repo.create_conversation(
        conversation_id,
        "Testing",
    )

    message_repo.add_message(
        conversation_id,
        "user",
        "Hello",
    )

    message_repo.add_message(
        conversation_id,
        "assistant",
        "Hi!",
    )

    messages = message_repo.get_messages(
        conversation_id
    )

    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"

    conversation_repo.delete_conversation(
        conversation_id
    )

    message_repo.close()
    conversation_repo.close()