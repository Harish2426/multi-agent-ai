import logging
import time
from uuid import uuid4


from app.graph import graph
from app.logging_context import get_request_id
from app.metrics import CHAT_COUNT
from services.conversation_service import (
    conversation_service,
)

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(
        self,
        conversation_service=conversation_service,
    ):
        self.conversation_service = (
            conversation_service
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

        started_at = time.perf_counter()
        CHAT_COUNT.inc()
        request_id = get_request_id()
        

        resolved_conversation_id = (
            conversation_id or str(uuid4())
        )

        created_conversation = False

        logger.info(
            "chat_started "
            "request_id=%s "
            "conversation_id=%s "
            "user_id=%s",
            request_id,
            resolved_conversation_id,
            user_id,
        )

        # --------------------------------------------------
        # Legacy / unauthenticated compatibility path
        # --------------------------------------------------

        if user_id is None:

            state = self.create_state(
                message=message,
                conversation_id=resolved_conversation_id,
            )

            try:
                result = graph.invoke(state)

            except Exception:

                duration_ms = (
                    time.perf_counter()
                    - started_at
                ) * 1000

                logger.exception(
                    "chat_failed "
                    "request_id=%s "
                    "conversation_id=%s "
                    "duration_ms=%.2f",
                    request_id,
                    resolved_conversation_id,
                    duration_ms,
                )

                raise

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            logger.info(
                "chat_completed "
                "request_id=%s "
                "conversation_id=%s "
                "route=%s "
                "duration_ms=%.2f",
                request_id,
                resolved_conversation_id,
                result["route"],
                duration_ms,
            )

            return {
                "response": result["final_answer"],
                "route": result["route"],
                "messages": result["messages"],
                "conversation_id": resolved_conversation_id,
            }

        # --------------------------------------------------
        # Authenticated path
        # --------------------------------------------------

        if conversation_id is None:

            self.conversation_service.conversations.create_conversation(
                conversation_id=resolved_conversation_id,
                title=message,
                user_id=user_id,
            )

            created_conversation = True

        else:

            conversation = (
                self.conversation_service
                .conversations
                .get_conversation(
                    resolved_conversation_id,
                    user_id=user_id,
                )
            )

            if conversation is None:

                logger.warning(
                    "chat_access_denied "
                    "request_id=%s "
                    "conversation_id=%s "
                    "user_id=%s",
                    request_id,
                    resolved_conversation_id,
                    user_id,
                )

                raise PermissionError(
                    "Conversation not found."
                )

        state = self.create_state(
            message=message,
            conversation_id=resolved_conversation_id,
        )

        try:

            result = graph.invoke(state)

            self.conversation_service.add_message_pair(
                conversation_id=resolved_conversation_id,
                user_content=message,
                assistant_content=result["final_answer"],
                route=result["route"],
            )

        except Exception:

            if created_conversation:

                try:

                    self.conversation_service.delete_conversation(
                        resolved_conversation_id,
                        user_id=user_id,
                    )

                except Exception:

                    logger.exception(
                        "chat_cleanup_failed "
                        "request_id=%s "
                        "conversation_id=%s "
                        "user_id=%s",
                        request_id,
                        resolved_conversation_id,
                        user_id,
                    )

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            logger.exception(
                "chat_failed "
                "request_id=%s "
                "conversation_id=%s "
                "user_id=%s "
                "duration_ms=%.2f",
                request_id,
                resolved_conversation_id,
                user_id,
                duration_ms,
            )

            raise

        duration_ms = (
            time.perf_counter()
            - started_at
        ) * 1000

        logger.info(
            "chat_completed "
            "request_id=%s "
            "conversation_id=%s "
            "user_id=%s "
            "route=%s "
            "duration_ms=%.2f",
            request_id,
            resolved_conversation_id,
            user_id,
            result["route"],
            duration_ms,
        )

        return {
            "response": result["final_answer"],
            "route": result["route"],
            "messages": result["messages"],
            "conversation_id": resolved_conversation_id,
        }


chat_service = ChatService()