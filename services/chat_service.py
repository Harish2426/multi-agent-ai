from uuid import uuid4

from app.graph import graph
from services.conversation_service import (
    ConversationService,
    conversation_service,
)


class ChatService:

    def __init__(
        self,
        conversation_service_instance: (
            ConversationService | None
        ) = None,
        **kwargs,
    ):
        # Accept the dependency keyword used by FastAPI while
        # preserving ChatService() compatibility.
        injected_service = kwargs.pop(
            "conversation_service",
            None,
        )

        if kwargs:
            unexpected = next(iter(kwargs))
            raise TypeError(
                f"Unexpected argument: {unexpected}"
            )

        self.conversation_service = (
            conversation_service_instance
            or injected_service
            or conversation_service
        )

    def create_state(
        self,
        message: str,
        conversation_id: str,
    ) -> dict:
        return {
            "user_input": message,
            "conversation_id": conversation_id,
            "messages": [],
            "route": "",
            "plan": "",
            "research": "",
            "code": "",
            "review": "",
            "tool_result": "",
            "memories": [],
            "final_answer": "",
        }

    def chat(
        self,
        message: str,
        conversation_id: str | None = None,
        user_id: str | None = None,
    ) -> dict:

        resolved_conversation_id = (
            conversation_id or str(uuid4())
        )

        created_new_conversation = False

        if user_id is not None:

            if conversation_id is not None:
                existing = (
                    self.conversation_service
                    .conversations
                    .get_conversation(
                        conversation_id,
                        user_id=user_id,
                    )
                )

                if existing is None:
                    raise PermissionError(
                        "Conversation not found."
                    )

            else:
                (
                    self.conversation_service
                    .conversations
                    .create_conversation(
                        conversation_id=(
                            resolved_conversation_id
                        ),
                        title=(
                            message[:60]
                            or "New Conversation"
                        ),
                        user_id=user_id,
                    )
                )

                created_new_conversation = True

        state = self.create_state(
            message=message,
            conversation_id=resolved_conversation_id,
        )

        try:
            result = graph.invoke(state)

        except Exception:
            if (
                user_id is not None
                and created_new_conversation
            ):
                self.conversation_service.delete_conversation(
                    resolved_conversation_id,
                    user_id=user_id,
                )

            raise

        if user_id is not None:
            try:
                self.conversation_service.add_message_pair(
                    conversation_id=(
                        resolved_conversation_id
                    ),
                    user_content=message,
                    assistant_content=(
                        result["final_answer"]
                    ),
                    route=result["route"],
                )

            except Exception:
                if created_new_conversation:
                    self.conversation_service.delete_conversation(
                        resolved_conversation_id,
                        user_id=user_id,
                    )

                raise

        return {
            "response": result["final_answer"],
            "route": result["route"],
            "messages": result["messages"],
            "conversation_id": resolved_conversation_id,
        }


chat_service = ChatService()