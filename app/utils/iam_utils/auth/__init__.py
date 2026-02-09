"""Authentication and authorization utilities.

JWT token management, password hashing, and FastAPI dependencies for auth.
"""

from app.utils.iam_utils.auth.auth_utils import AuthUtils, auth_utils
from app.utils.iam_utils.auth.jwt_utils import JWTUtils, JWT_utils, JWTError
from app.utils.iam_utils.auth.auth_deps import TokenPayload, get_current_user_payload

__all__ = [
    # Classes
    "AuthUtils",
    "JWTUtils",
    "JWTError",
    "TokenPayload",
    # Instances
    "auth_utils",
    "JWT_utils",
    # Dependencies
    "get_current_user_payload",
]

