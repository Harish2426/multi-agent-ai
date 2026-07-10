from uuid import uuid4

import pytest

from database.repositories.conversation_repository import (
    ConversationRepository,
)
from database.repositories.user_repository import (
    UserRepository,
)


@pytest.fixture
def repositories():
    users = UserRepository()
    conversations = ConversationRepository()

    yield users, conversations

    conversations.close()


def create_user(
    users: UserRepository,
    email_prefix: str,
):
    return users.create_user(
        email=f"{email_prefix}-{uuid4()}@example.com",
        password_hash="test-password-hash",
    )


def test_user_can_get_own_conversation(
    repositories,
):
    users, conversations = repositories

    user = create_user(users, "owner")

    conversation = conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Owner Conversation",
        user_id=user.id,
    )

    result = conversations.get_conversation(
        conversation.id,
        user_id=user.id,
    )

    assert result is not None
    assert result.id == conversation.id
    assert result.user_id == user.id


def test_user_cannot_get_another_users_conversation(
    repositories,
):
    users, conversations = repositories

    owner = create_user(users, "owner")
    other_user = create_user(users, "other")

    conversation = conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Private Conversation",
        user_id=owner.id,
    )

    result = conversations.get_conversation(
        conversation.id,
        user_id=other_user.id,
    )

    assert result is None


def test_list_conversations_is_user_scoped(
    repositories,
):
    users, conversations = repositories

    user_a = create_user(users, "user-a")
    user_b = create_user(users, "user-b")

    conversation_a = conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Conversation A",
        user_id=user_a.id,
    )

    conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Conversation B",
        user_id=user_b.id,
    )

    results = conversations.list_conversations(
        user_id=user_a.id,
    )

    result_ids = {
        conversation.id
        for conversation in results
    }

    assert conversation_a.id in result_ids

    assert all(
        conversation.user_id == user_a.id
        for conversation in results
    )


def test_user_cannot_rename_another_users_conversation(
    repositories,
):
    users, conversations = repositories

    owner = create_user(users, "owner")
    other_user = create_user(users, "other")

    conversation = conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Original Title",
        user_id=owner.id,
    )

    result = conversations.update_title(
        conversation_id=conversation.id,
        title="Unauthorized Rename",
        user_id=other_user.id,
    )

    assert result is None

    unchanged = conversations.get_conversation(
        conversation.id,
        user_id=owner.id,
    )

    assert unchanged is not None
    assert unchanged.title == "Original Title"


def test_user_cannot_delete_another_users_conversation(
    repositories,
):
    users, conversations = repositories

    owner = create_user(users, "owner")
    other_user = create_user(users, "other")

    conversation = conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Private Conversation",
        user_id=owner.id,
    )

    deleted = conversations.delete_conversation(
        conversation_id=conversation.id,
        user_id=other_user.id,
    )

    assert deleted is False

    existing = conversations.get_conversation(
        conversation.id,
        user_id=owner.id,
    )

    assert existing is not None


def test_owner_can_delete_own_conversation(
    repositories,
):
    users, conversations = repositories

    owner = create_user(users, "owner")

    conversation = conversations.create_conversation(
        conversation_id=str(uuid4()),
        title="Delete Me",
        user_id=owner.id,
    )

    deleted = conversations.delete_conversation(
        conversation_id=conversation.id,
        user_id=owner.id,
    )

    assert deleted is True

    existing = conversations.get_conversation(
        conversation.id,
        user_id=owner.id,
    )

    assert existing is None