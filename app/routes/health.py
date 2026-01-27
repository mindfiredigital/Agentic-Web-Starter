from fastapi import Request, APIRouter, HTTPException, status
from app.config.log_config import logger
from app.schemas.health import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Return application health status.

    Args:
        request: Incoming request.

    Returns:
        HealthResponse payload.
    """
    try:
        logger.info(f"Health check: {request.url}")
        return {"message": "Up and running"}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unhandled error while checking health: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed",
        )
