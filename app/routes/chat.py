from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.agents.supervisor import SupervisorAgent


router = APIRouter()
supervisor = SupervisorAgent()


class ChatRequest(BaseModel):
    thread_id: str = Field(..., description="Conversation thread id")
    message: str = Field(..., description="User message")


@router.post("/chat")
async def chat(request: ChatRequest):
    answer = supervisor.handle(thread_id=request.thread_id, query=request.message)
    return {"thread_id": request.thread_id, "answer": answer}
