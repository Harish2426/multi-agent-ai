from datetime import datetime, timezone
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

    def _next_sequence(
        self,
        conversation_id: str,
    ) -> int:
        result = self.collection.get(
            where={
                "conversation_id": conversation_id
            },
            include=["metadatas"],
        )

        metadatas = result.get("metadatas") or []

        sequences = [
            metadata.get("sequence", 0)
            for metadata in metadatas
            if metadata
        ]

        return max(sequences, default=0) + 1

    def add(
        self,
        conversation_id: str,
        user_input: str,
        assistant_response: str,
    ) -> None:
        first_sequence = self._next_sequence(
            conversation_id
        )

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        self.collection.add(
            ids=[
                str(uuid4()),
                str(uuid4()),
            ],
            documents=[
                user_input,
                assistant_response,
            ],
            metadatas=[
                {
                    "conversation_id": conversation_id,
                    "role": "user",
                    "timestamp": timestamp,
                    "sequence": first_sequence,
                },
                {
                    "conversation_id": conversation_id,
                    "role": "assistant",
                    "timestamp": timestamp,
                    "sequence": first_sequence + 1,
                },
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

        documents = result.get("documents") or []

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
            metadata = metadata or {}

            # Ignore legacy records created before structured memory.
            if (
                "role" not in metadata
                or "timestamp" not in metadata
                or "sequence" not in metadata
            ):
                continue

            history_items.append(
                {
                    "id": document_id,
                    "role": metadata["role"],
                    "content": document,
                    "timestamp": metadata["timestamp"],
                    "sequence": metadata["sequence"],
                }
            )

        history_items.sort(
            key=lambda item: item["sequence"]
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