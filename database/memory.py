from uuid import uuid4

import chromadb


class ConversationMemory:

    def __init__(
        self,
        path: str = "database/vector_db",
        collection_name: str = "conversations",
    ):
        self.client = chromadb.PersistentClient(path=path)

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        conversation_id: str,
        user_input: str,
        assistant_response: str,
    ) -> None:
        document_id = str(uuid4())

        document = (
            f"User: {user_input}\n"
            f"Assistant: {assistant_response}"
        )

        self.collection.add(
            ids=[document_id],
            documents=[document],
            metadatas=[
                {
                    "conversation_id": conversation_id,
                    "user_input": user_input,
                }
            ],
        )

    def search(
        self,
        conversation_id: str,
        query: str,
        limit: int = 3,
    ) -> list[str]:
        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={
                "conversation_id": conversation_id
            },
        )

        documents = result.get("documents")

        if not documents:
            return []

        return documents[0]

    def history(
        self,
        conversation_id: str,
    ) -> list[dict]:
        result = self.collection.get(
            where={
                "conversation_id": conversation_id
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        ids = result.get("ids") or []
        documents = result.get("documents") or []
        metadatas = result.get("metadatas") or []

        history_items = []

        for document_id, document, metadata in zip(
            ids,
            documents,
            metadatas,
        ):
            history_items.append(
                {
                    "id": document_id,
                    "document": document,
                    "metadata": metadata or {},
                }
            )

        return history_items

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> int:
        existing = self.collection.get(
            where={
                "conversation_id": conversation_id
            },
            include=[],
        )

        ids = existing.get("ids") or []

        if not ids:
            return 0

        self.collection.delete(ids=ids)

        return len(ids)


memory = ConversationMemory()