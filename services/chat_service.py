from app.graph import graph


class ChatService:

    def create_state(self, message: str) -> dict:

        return {
            "user_input": message,
            "messages": [],

            "route": "",

            "plan": "",
            "research": "",
            "code": "",
            "review": "",

            "final_answer": "",
        }

    def chat(self, message: str) -> dict:

        state = self.create_state(message)

        result = graph.invoke(state)

        return {
            "response": result["final_answer"],
            "route": result["route"],
            "messages": result["messages"],
        }


chat_service = ChatService()