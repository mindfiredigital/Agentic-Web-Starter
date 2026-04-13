import os

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.env_config import settings
from app.config.log_config import logger
from app.constants.app_constants import ROUTE_CONSTANTS
from app.exceptions import AppError
from app.exceptions.handlers import (
    app_error_handler,
    global_exception_handler,
    http_exception_handler,
    request_validation_handler,
)
from app.health import router as health_router
from app.routes.core_routes.router import router as core_router
from app.utils.core_utils import init_db, sqlite_db


def start_application():
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI app instance with middleware, routers, and DB init.
    """
    logger.info("Starting application...")
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        root_path=settings.BASE_PATH,
        # contact = {"name":"Mindfire Solutions", "url":"https://www.mindfire.com", "email":"support@mindfire.com"},
    )

    # PATH HANDLING
    if settings.USE_SQL:
        os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # DATABASE INITIALIZATION
    if settings.USE_SQL:
        try:
            init_db()
        except Exception as e:
            logger.exception("Database initialization failed: %s", e)
            raise
        try:
            _bootstrap_admin_user()
        except Exception as e:
            logger.exception("Admin bootstrap failed: %s", e)
            raise
    else:
        logger.info(
            "SQL disabled. Skipping database initialization and admin bootstrap."
        )

    # EXCEPTION HANDLERS
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # CORS MIDDLEWARE
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ROUTERS
    app.include_router(health_router)
    api_v1 = APIRouter(prefix=ROUTE_CONSTANTS.API_V1_PREFIX.value)

    if settings.USE_SQL:
        from app.routes.iam_routes.router import router as iam_router

        api_v1.include_router(iam_router)
    else:
        logger.info("SQL disabled. IAM routes are not registered.")

    api_v1.include_router(core_router)
    app.include_router(api_v1)

    logger.info("Application started successfully")

    return app


def _bootstrap_admin_user() -> None:
    """Create the initial admin user from environment variables."""
    from app.services.iam_services.auth_service import AuthService

    if not settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD:
        logger.info("Admin bootstrap skipped: ADMIN_USERNAME/PASSWORD not set")
        return

    db = sqlite_db.connect()
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
