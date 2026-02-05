from fastapi import APIRouter, HTTPException, status

from app.agents.supervisor_agent import supervisor
from app.config.log_config import logger
from app.schemas.chat_schema import ChatRequest, ChatResponse


router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat requests using the supervisor agent.

    Args:
        request: Chat request payload.

    Returns:
        ChatResponse payload.
    """
    try:
        answer = supervisor.invoke(thread_id=request.thread_id, query=request.query)
        return {"thread_id": request.thread_id, "answer": answer}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unhandled error while handling chat: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chat request failed",
        )
