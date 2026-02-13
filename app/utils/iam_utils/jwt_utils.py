import jwt
from typing import List
from datetime import datetime, timedelta, timezone

from app.config.env_config import settings


class JWTError(Exception):
    """Raised when a JWT cannot be validated."""

    def __init__(self, message: str) -> None:
        """Initialize JWTError with a message.

        Args:
            message: Human-readable error description.
        """
        self.message = message
        super().__init__(self.message)


class JWTUtils:
    """Utility class for JWT operations."""

    def __init__(self) -> None:
        """Initialize JWT utils from application settings."""
        self.jwt = jwt
        self.jwt_secret_key = settings.JWT_SECRET_KEY
        self.jwt_algorithm = settings.JWT_ALGORITHM
        self.jwt_access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, user_id: str, role_ids: List[str], expires_minutes: int | None = None) -> str:
        """Create a signed JWT access token.

        Args:
            user_id: Subject (user) identifier.
            role_ids: List of role IDs to embed in token.
            expires_minutes: Token expiry in minutes. Defaults to settings value.

        Returns:
            Encoded JWT string.
        """
        if expires_minutes is None:
            expires_minutes = self.jwt_access_token_expire_minutes

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

        payload = {
            "sub": str(user_id),
            "role_ids": role_ids,
            "exp": expires_at,
        }

        return self.jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

    def decode_access_token(self, token: str) -> dict:
        """Decode and validate a JWT access token.

        Args:
            token: Encoded JWT string.

        Returns:
            Decoded payload dict (sub, role_ids, exp, etc.).

        Raises:
            JWTError: If token is expired or invalid.
        """
        try:
            return self.jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
        except jwt.ExpiredSignatureError as exc:
            raise JWTError("Token expired") from exc
        except jwt.InvalidTokenError as exc:
            raise JWTError("Invalid token") from exc


JWT_utils = JWTUtils()
