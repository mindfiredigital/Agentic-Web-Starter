from fastapi import APIRouter, HTTPException, status

from app.agents.supervisor import SupervisorAgent
from app.config.logger import logger
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter()
supervisor = SupervisorAgent()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = supervisor.handle(thread_id=request.thread_id, query=request.query)
        return {"thread_id": request.thread_id, "answer": answer}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unhandled error while handling chat: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chat request failed",
        )
