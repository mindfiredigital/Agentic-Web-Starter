import uvicorn
from fastapi import FastAPI
from src.config.logger import logger
from src.routes.health import router as health_router
from src.routes.chat import router as chat_router
from src.routes.ingest import router as ingest_router
from src.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

def start_application():
    logger.info("Starting application...")
    app = FastAPI(
        title = settings.PROJECT_NAME,
        version = settings.PROJECT_VERSION,
        description = settings.PROJECT_DESCRIPTION,
        root_path = settings.BASE_PATH,
        contact = {"name":"Mindfire Solutions", "url":"https://www.mindfire.com", "email":"support@mindfire.com"},
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(health_router)
    api_v1.include_router(chat_router)
    api_v1.include_router(ingest_router)
    app.include_router(api_v1)

    logger.info("Application started successfully")

    return app

app = start_application()