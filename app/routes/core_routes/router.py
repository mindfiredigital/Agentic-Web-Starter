from fastapi import APIRouter

from app.routes.core_routes.chat_route import router as chat_router
from app.routes.core_routes.ingestion_route import router as ingestion_router

router = APIRouter()
router.include_router(chat_router)
router.include_router(ingestion_router)

