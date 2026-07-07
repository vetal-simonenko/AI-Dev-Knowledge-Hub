from app.llm.client import ask_llm


class ChatService:
    def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:
        return ask_llm(session_id, message)
