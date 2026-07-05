from database.memory import memory


class MemoryService:

    def get_history(
        self,
        conversation_id: str,
    ) -> list[dict]:
        return memory.history(
            conversation_id=conversation_id
        )

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> int:
        return memory.delete_conversation(
            conversation_id=conversation_id
        )


memory_service = MemoryService()