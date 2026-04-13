from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    thread_id: str = Field(..., description="Conversation thread id")
    query: str = Field(..., description="User query")


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    thread_id: str = Field(..., description="Conversation thread id")
    answer: str = Field(..., description="Assistant response")
