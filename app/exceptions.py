class DomainError(Exception):
    """Base domain exception."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class AuthenticationError(DomainError):
    """Raised when credentials are invalid or missing."""


class PermissionDeniedError(DomainError):
    """Raised when access is not permitted."""


class NotFoundError(DomainError):
    """Raised when a resource cannot be found."""


class DomainValidationError(DomainError):
    """Raised when a domain validation rule fails."""
