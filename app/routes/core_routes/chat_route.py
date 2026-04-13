from fastapi import APIRouter

from app.agents.supervisor_agent import supervisor
from app.schemas.core_schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat requests using the supervisor agent.

    Args:
        request: ChatRequest with thread_id and query.

    Returns:
        ChatResponse with thread_id and agent answer.

    Exceptions handled by global handlers.
    """
    answer = supervisor.invoke(thread_id=request.thread_id, query=request.query)
    return {"thread_id": request.thread_id, "answer": answer}
