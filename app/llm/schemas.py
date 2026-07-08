from pydantic import BaseModel, Field


class LLMChatResponse(BaseModel):
    answer: str
    topic: str
    confidence: float = Field(ge=0, le=1)
