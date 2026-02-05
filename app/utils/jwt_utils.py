from datetime import datetime, timedelta, timezone
from typing import List

import jwt

from app.config.env_config import settings


class JWTError(Exception):
    """Raised when a JWT cannot be validated."""


def create_access_token(user_id: str, role_ids: List[str], expires_minutes: int | None = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": user_id,
        "role_ids": role_ids,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError as exc:
        raise JWTError("Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise JWTError("Invalid token") from exc
