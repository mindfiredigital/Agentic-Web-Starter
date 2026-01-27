from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from app.config.logger import logger

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    logger.info(f"Health check: {request.url}")
    return JSONResponse(status_code=200, content={"message": "Up and running"})
