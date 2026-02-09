from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: str = Field(..., description="Conversation thread id")
    query: str = Field(..., description="User query")


class ChatResponse(BaseModel):
    thread_id: str = Field(..., description="Conversation thread id")
    answer: str = Field(..., description="Assistant response")

