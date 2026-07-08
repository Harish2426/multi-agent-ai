import uuid

from database.repositories.conversation_repository import (
    ConversationRepository,
)


def test_create_conversation():

    repo = ConversationRepository()

    conversation_id = str(uuid.uuid4())

    conversation = repo.create_conversation(
        conversation_id,
        "My First Chat",
    )

    assert conversation.id == conversation_id
    assert conversation.title == "My First Chat"

    repo.close()


def test_get_conversation():

    repo = ConversationRepository()

    conversation_id = str(uuid.uuid4())

    repo.create_conversation(
        conversation_id,
        "Chat",
    )

    conversation = repo.get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation.id == conversation_id

    repo.close()


def test_update_title():

    repo = ConversationRepository()

    conversation_id = str(uuid.uuid4())

    repo.create_conversation(
        conversation_id,
        "Old",
    )

    updated = repo.update_title(
        conversation_id,
        "New",
    )

    assert updated.title == "New"

    repo.close()


def test_delete_conversation():

    repo = ConversationRepository()

    conversation_id = str(uuid.uuid4())

    repo.create_conversation(
        conversation_id,
        "Delete Me",
    )

    deleted = repo.delete_conversation(
        conversation_id
    )

    assert deleted

    conversation = repo.get_conversation(
        conversation_id
    )

    assert conversation is None

    repo.close()