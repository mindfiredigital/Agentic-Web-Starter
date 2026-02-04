import os
import uvicorn
from fastapi import FastAPI
from app.config.log_config import logger
from app.health import router as health_router
from app.routes.chat_route import router as chat_router
from app.routes.ingestion_route import router as ingestion_router
from app.config.env_config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

def start_application():
    """Create and configure the FastAPI application."""
    logger.info("Starting application...")
    app = FastAPI(
        title = settings.PROJECT_NAME,
        version = settings.PROJECT_VERSION,
        description = settings.PROJECT_DESCRIPTION,
        root_path = settings.BASE_PATH,
        # contact = {"name":"Mindfire Solutions", "url":"https://www.mindfire.com", "email":"support@mindfire.com"},
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(chat_router)
    api_v1.include_router(ingestion_router)
    app.include_router(api_v1)


    # PATH HANDLING 
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    logger.info("Application started successfully")

    return app