import sqlite3

from fastapi import APIRouter, Depends, status

from app.schemas.iam_schemas.auth_schema import LoginRequest, TokenResponse
from app.services.iam_services.auth_service import AuthService
from app.utils.core_utils import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    request: LoginRequest, db: sqlite3.Connection = Depends(get_db)
) -> TokenResponse:
    """Authenticate user and return JWT.

    Args:
        request: LoginRequest with username and password.
        db: Database connection (injected).

    Returns:
        TokenResponse with access_token.

    Exceptions handled by global handlers.
    """
    service = AuthService(db)
    token = service.login(username=request.username, password=request.password)
    return TokenResponse(access_token=token)
