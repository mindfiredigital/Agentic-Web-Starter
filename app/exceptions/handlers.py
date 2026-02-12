import asyncio
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.log_config import logger
from app.exceptions.domain import AppError


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic request validation errors (422).

    Args:
        request: The FastAPI request.
        exc: The validation error exception.

    Returns:
        JSONResponse with 422 status and validation details.
    """
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
    """Handle FastAPI/Starlette HTTPException.

    Args:
        request: The FastAPI request.
        exc: The HTTP exception.

    Returns:
        JSONResponse with exception status and detail.
    """
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
    """Handle domain AppError and subclasses (response shape from domain).

    Args:
        request: The FastAPI request.
        exc: The domain AppError instance.

    Returns:
        JSONResponse with status_code and content from exc.to_response_content().
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response_content(request.url.path),
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unhandled exceptions; log and return safe 500 response.

    Args:
        request: The FastAPI request.
        exc: The unhandled exception.

    Returns:
        JSONResponse with 500 status and generic error message.
    """
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
    """Re-raise CancelledError so it is not logged as an unhandled exception.

    Args:
        request: The FastAPI request.
        exc: The CancelledError (re-raised).
    """
    raise exc
