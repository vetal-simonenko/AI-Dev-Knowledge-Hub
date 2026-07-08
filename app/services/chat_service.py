from app.llm.llm_client import LLMClient
from app.schemas.chat import ChatResponse


class ChatService:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def chat(
        self,
        session_id: str,
        message: str,
    ) -> ChatResponse:
        llm_response = self.llm_client.ask(session_id, message)

        return ChatResponse(
            answer=llm_response.answer,
            topic=llm_response.topic,
            confidence=llm_response.confidence,
        )
