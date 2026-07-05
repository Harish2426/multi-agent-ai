from database.memory import ConversationMemory


def test_structured_history(tmp_path):
    memory = ConversationMemory(
        path=str(tmp_path / "chroma"),
        collection_name="test_conversations",
    )

    memory.add(
        conversation_id="conversation-a",
        user_input="Hello",
        assistant_response="Hi there",
    )

    history = memory.history(
        "conversation-a"
    )

    assert len(history) == 2

    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[0]["sequence"] == 1

    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there"
    assert history[1]["sequence"] == 2


def test_history_ordering(tmp_path):
    memory = ConversationMemory(
        path=str(tmp_path / "chroma"),
        collection_name="test_ordering",
    )

    memory.add(
        "conversation-a",
        "First question",
        "First answer",
    )

    memory.add(
        "conversation-a",
        "Second question",
        "Second answer",
    )

    history = memory.history(
        "conversation-a"
    )

    assert [
        item["sequence"]
        for item in history
    ] == [1, 2, 3, 4]


def test_conversation_isolation(tmp_path):
    memory = ConversationMemory(
        path=str(tmp_path / "chroma"),
        collection_name="test_isolation",
    )

    memory.add(
        "conversation-a",
        "Question A",
        "Answer A",
    )

    memory.add(
        "conversation-b",
        "Question B",
        "Answer B",
    )

    history_a = memory.history(
        "conversation-a"
    )

    history_b = memory.history(
        "conversation-b"
    )

    assert len(history_a) == 2
    assert len(history_b) == 2

    assert all(
        "A" in item["content"]
        for item in history_a
    )

    assert all(
        "B" in item["content"]
        for item in history_b
    )


def test_delete_structured_conversation(tmp_path):
    memory = ConversationMemory(
        path=str(tmp_path / "chroma"),
        collection_name="test_deletion",
    )

    memory.add(
        "conversation-a",
        "Hello",
        "Hi",
    )

    deleted_count = memory.delete_conversation(
        "conversation-a"
    )

    assert deleted_count == 2

    assert memory.history(
        "conversation-a"
    ) == []