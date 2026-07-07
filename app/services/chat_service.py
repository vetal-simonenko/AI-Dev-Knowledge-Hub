from app.llm.client import ask_llm

class ChatService:

    def chat(self, message: str) -> str:
        return ask_llm(message)
    



