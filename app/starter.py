import os
import uvicorn
from fastapi import FastAPI, Request
from app.config.log_config import logger
from app.health import router as health_router
from app.routes.chat_route import router as chat_router
from app.routes.ingestion_route import router as ingestion_router
from app.routes.auth_route import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.role_routes import router as role_router
from app.config.env_config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.exceptions import (
    AuthenticationError,
    DomainValidationError,
    NotFoundError,
    PermissionDeniedError,
)
from app.repository.sqlite_repository import init_db, _connect
from app.services.auth_service import AuthService

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

    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    init_db()
    _bootstrap_admin_user()

    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(status_code=401, content={"detail": exc.message})

    @app.exception_handler(PermissionDeniedError)
    async def permission_error_handler(request: Request, exc: PermissionDeniedError):
        return JSONResponse(status_code=403, content={"detail": exc.message})

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(DomainValidationError)
    async def validation_error_handler(request: Request, exc: DomainValidationError):
        return JSONResponse(status_code=422, content={"detail": exc.message})
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(auth_router)
    api_v1.include_router(chat_router)
    api_v1.include_router(ingestion_router)
    api_v1.include_router(user_router)
    api_v1.include_router(role_router)
    app.include_router(api_v1)


    # PATH HANDLING 
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    logger.info("Application started successfully")

    return app

def _bootstrap_admin_user() -> None:
    """Create the initial admin user from environment variables."""
    if not settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD:
        logger.info("Admin bootstrap skipped: ADMIN_USERNAME/PASSWORD not set")
        return

    db = _connect()
    try:
        service = AuthService(db)
        created = service.bootstrap_admin(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
        )
        if created:
            logger.info("Admin bootstrap completed")
        else:
            logger.info("Admin bootstrap skipped: users already exist")
    finally:
        db.close()