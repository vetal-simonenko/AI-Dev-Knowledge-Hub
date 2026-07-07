from fastapi import FastAPI

from app.llm.client import ask_llm
from app.schemas.chat import ChatRequest, ChatResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI Dev Knowledge Hub API"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = ask_llm(request.message)

    return ChatResponse(answer=answer)