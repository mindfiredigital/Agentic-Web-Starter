class AppError(Exception):
    """Base application error with HTTP status and error code."""

    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str) -> None:
        """Initialize AppError with a message.

        Args:
            message: Human-readable error description.
        """
        super().__init__(message)
        self.message = message

    def to_response_content(self, path: str) -> dict:
        """Build the JSON body for this error (used by handlers).

        Args:
            path: Request path for the response.

        Returns:
            Dict with error code, message, and path.
        """
        return {
            "error": {"code": self.code, "message": self.message},
            "path": path,
        }


class UnauthorizedError(AppError):
    """Credentials invalid or missing."""

    status_code = 401
    code = "unauthorized"


class ForbiddenError(AppError):
    """Access not permitted."""

    status_code = 403
    code = "forbidden"


class NotFoundError(AppError):
    """Resource not found."""

    status_code = 404
    code = "not_found"


class ConflictError(AppError):
    """Resource already exists or conflicts."""

    status_code = 409
    code = "conflict"


class ValidationError(AppError):
    """Domain or request validation failed."""

    status_code = 422
    code = "validation_error"


class InternalError(AppError):
    """Unexpected internal error (e.g. DB, I/O)."""

    status_code = 500
    code = "internal_error"
