import sqlite3
from typing import List

from fastapi import APIRouter, Depends, status

from app.utils.core_utils.database import get_db
from app.utils.iam_utils.auth import get_current_user_payload, TokenPayload
from app.services.iam_services.role_service import RoleService
from app.schemas.iam_schemas.role_schema import RoleCreate, RoleResponse, RoleUpdate

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/list_roles", response_model=List[RoleResponse])
def list_roles(payload: TokenPayload = Depends(get_current_user_payload), db: sqlite3.Connection = Depends(get_db)) -> List[RoleResponse]:
    """List roles (requires component access).

    Args:
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        List of RoleResponse.

    Exceptions handled by global handlers.
    """
    service = RoleService(db)
    return service.list_roles(role_ids=payload.role_ids)


@router.get("/get_role/{role_id}", response_model=RoleResponse)
def get_role(role_id: str, payload: TokenPayload = Depends(get_current_user_payload), db: sqlite3.Connection = Depends(get_db)) -> RoleResponse:
    """Get role by id.

    Args:
        role_id: Role identifier.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        RoleResponse for the role.

    Exceptions handled by global handlers.
    """
    service = RoleService(db)
    return service.get_role(role_id=role_id, role_ids=payload.role_ids)


@router.post("/create_role", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(request: RoleCreate, payload: TokenPayload = Depends(get_current_user_payload), db: sqlite3.Connection = Depends(get_db)) -> RoleResponse:
    """Create role.

    Args:
        request: RoleCreate with name and optional description.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        RoleResponse for created role.

    Exceptions handled by global handlers.
    """
    service = RoleService(db)
    return service.create_role(
        name=request.name,
        description=request.description,
        current_user_id=payload.sub,
        role_ids=payload.role_ids,
    )


@router.put("/update_role/{role_id}", response_model=RoleResponse)
def update_role(role_id: str, request: RoleUpdate, payload: TokenPayload = Depends(get_current_user_payload), db: sqlite3.Connection = Depends(get_db)) -> RoleResponse:
    """Update role.

    Args:
        role_id: Role identifier.
        request: RoleUpdate with optional name and description.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        RoleResponse for updated role.

    Exceptions handled by global handlers.
    """
    service = RoleService(db)
    return service.update_role(
        role_id=role_id,
        name=request.name,
        description=request.description,
        current_user_id=payload.sub,
        role_ids=payload.role_ids,
    )


@router.delete("/delete_role/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(role_id: str, payload: TokenPayload = Depends(get_current_user_payload), db: sqlite3.Connection = Depends(get_db)) -> dict:
    """Delete role.

    Args:
        role_id: Role identifier.
        payload: Decoded JWT (injected).
        db: Database connection (injected).

    Returns:
        Dict with "detail": "Role deleted".

    Exceptions handled by global handlers.
    """
    service = RoleService(db)
    service.delete_role(role_id=role_id, role_ids=payload.role_ids)
    return {"detail": "Role deleted"}

