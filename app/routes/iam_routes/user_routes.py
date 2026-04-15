import sqlite3
from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.iam_schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.iam_services.user_service import UserService
from app.utils.core_utils import get_db
from app.utils.iam_utils import TokenPayload, get_current_user_payload

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/list_users", response_model=List[UserResponse])
def list_users(
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> List[UserResponse]:
    """List users (requires component access).

    Args:
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        List of UserResponse.

    Exceptions handled by global handlers.
    """
    service = UserService(db)
    return service.list_users(role_ids=payload.role_ids)


@router.get("/get_user/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> UserResponse:
    """Get user by id.

    Args:
        user_id: User identifier.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        UserResponse for the user.

    Exceptions handled by global handlers.
    """
    service = UserService(db)
    return service.get_user(user_id=user_id, role_ids=payload.role_ids)


@router.post(
    "/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    request: UserCreate,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> UserResponse:
    """Create user.

    Args:
        request: UserCreate with username, email, password.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        UserResponse for created user.

    Exceptions handled by global handlers.
    """
    service = UserService(db)
    return service.create_user(
        username=request.username,
        email=request.email,
        password=request.password,
        current_user_id=payload.sub,
        role_ids=payload.role_ids,
    )


@router.put("/update_user/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    request: UserUpdate,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> UserResponse:
    """Update user.

    Args:
        user_id: User identifier.
        request: UserUpdate with optional username, email, password.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        UserResponse for updated user.

    Exceptions handled by global handlers.
    """
    service = UserService(db)
    return service.update_user(
        user_id=user_id,
        username=request.username,
        email=request.email,
        password=request.password,
        current_user_id=payload.sub,
        role_ids=payload.role_ids,
    )


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: str,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> dict:
    """Delete user.

    Args:
        user_id: User identifier.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        Dict with "detail": "User deleted".

    Exceptions handled by global handlers.
    """
    service = UserService(db)
    service.delete_user(user_id=user_id, role_ids=payload.role_ids)
    return {"detail": "User deleted"}
