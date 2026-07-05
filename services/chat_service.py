from app.graph import graph
from app.models import ModelError

from services.error_handler import model_error_message


class ChatService:

    def create_state(
        self,
        message: str,
    ) -> dict:

        return {
            "user_input": message,
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
    ) -> dict:

        state = self.create_state(message)

        try:
            result = graph.invoke(state)

            return {
                "response": result["final_answer"],
                "route": result["route"],
                "messages": result["messages"],
            }

        except ModelError as error:

            return {
                "response": model_error_message(error),
                "route": "error",
                "messages": [
                    f"Model failure: {type(error).__name__}"
                ],
            }


chat_service = ChatService()