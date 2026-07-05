from uuid import uuid4

import chromadb


class ConversationMemory:

    def __init__(
        self,
        path: str = "database/vector_db",
        collection_name: str = "conversations",
    ):
        self.client = chromadb.PersistentClient(
            path=path
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add(
        self,
        user_input: str,
        assistant_response: str,
    ) -> None:

        document = (
            f"User: {user_input}\n"
            f"Assistant: {assistant_response}"
        )

        self.collection.add(
            ids=[str(uuid4())],
            documents=[document],
            metadatas=[
                {
                    "user_input": user_input,
                }
            ],
        )

    def search(
        self,
        query: str,
        limit: int = 3,
    ) -> list[str]:

        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_texts=[query],
            n_results=limit,
        )

        documents = result.get("documents")

        if not documents:
            return []

        return documents[0]


memory = ConversationMemory()