from app.llm.client import ask_llm
from app.schemas.chat import ChatResponse


class ChatService:
    def chat(
        self,
        session_id: str,
        message: str,
    ) -> ChatResponse:
        llm_response = ask_llm(session_id, message)

        return ChatResponse(
            answer=llm_response.answer,
            topic=llm_response.topic,
            confidence=llm_response.confidence,
        )
