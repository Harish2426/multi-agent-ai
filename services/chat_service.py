from uuid import uuid4

from app.graph import graph
from app.models import ModelError

from services.error_handler import model_error_message


class ChatService:

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
    ) -> dict:
        resolved_conversation_id = (
            conversation_id
            or str(uuid4())
        )

        state = self.create_state(
            message=message,
            conversation_id=resolved_conversation_id,
        )

        result = graph.invoke(state)

        return {
            "response": result["final_answer"],
            "route": result["route"],
            "messages": result["messages"],
            "conversation_id": resolved_conversation_id,
        }


chat_service = ChatService()