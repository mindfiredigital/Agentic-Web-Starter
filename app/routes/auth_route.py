import sqlite3

from fastapi import APIRouter, Depends, status

from app.repository.sqlite_repository import get_db
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: sqlite3.Connection = Depends(get_db)) -> TokenResponse:
    """Authenticate user and return JWT. Exceptions handled by global handlers."""
    service = AuthService(db)
    token = service.login(username=request.username, password=request.password)
    return TokenResponse(access_token=token)
