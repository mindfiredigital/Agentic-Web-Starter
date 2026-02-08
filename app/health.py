from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from app.config.log_config import logger

router = APIRouter()


class HealthResponse(BaseModel):
    message: str = Field(..., description="Health status message")


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Return application health status. Exceptions handled by global handlers."""
    logger.info("Health check: %s", request.url)
    return HealthResponse(message="Up and running")
