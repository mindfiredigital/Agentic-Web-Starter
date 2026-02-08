import asyncio
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.log_config import logger
from app.exceptions.domain import AppError


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic request validation errors (422)."""
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Validation error",
                "details": exc.errors(),
            },
            "path": request.url.path,
        },
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle FastAPI/Starlette HTTPException."""
    status_code = exc.status_code
    detail = exc.detail
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": "http_error",
                "message": detail,
            },
            "path": request.url.path,
        },
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle domain AppError and subclasses (response shape from domain)."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response_content(request.url.path),
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unhandled exceptions; log and return safe 500 response."""
    logger.exception(
        "Unhandled exception",
        extra={"path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "Internal Server Error",
            },
            "path": request.url.path,
        },
    )


async def cancelled_error_handler(request: Request, exc: asyncio.CancelledError) -> None:
    """Re-raise CancelledError so it is not logged as an unhandled exception."""
    raise exc
