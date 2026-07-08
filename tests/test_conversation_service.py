from services.conversation_service import conversation_service


def test_create_conversation():

    conversation = conversation_service.create(
        "Demo Chat"
    )

    assert conversation.title == "Demo Chat"

    conversation_service.delete(
        conversation.id
    )


def test_add_messages():

    conversation = conversation_service.create(
        "Messages"
    )

    conversation_service.add_user_message(
        conversation.id,
        "Hello",
    )

    conversation_service.add_assistant_message(
        conversation.id,
        "Hi!",
        "planner",
    )

    history = conversation_service.history(
        conversation.id
    )

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"

    conversation_service.delete(
        conversation.id
    )