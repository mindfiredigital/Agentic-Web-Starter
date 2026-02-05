from typing import List

from fastapi import APIRouter, Depends, status
import sqlite3

from app.repository.sqlite_repository import get_db
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.role_service import RoleService
from app.utils.auth_deps import TokenPayload, get_current_user_payload


router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=List[RoleResponse])
def list_roles(
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> List[RoleResponse]:
    service = RoleService(db)
    return service.list_roles(role_ids=payload.role_ids)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: str,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> RoleResponse:
    service = RoleService(db)
    return service.get_role(role_id=role_id, role_ids=payload.role_ids)


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    request: RoleCreate,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> RoleResponse:
    service = RoleService(db)
    return service.create_role(
        name=request.name,
        description=request.description,
        current_user_id=payload.sub,
        role_ids=payload.role_ids,
    )


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: str,
    request: RoleUpdate,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> RoleResponse:
    service = RoleService(db)
    return service.update_role(
        role_id=role_id,
        name=request.name,
        description=request.description,
        current_user_id=payload.sub,
        role_ids=payload.role_ids,
    )


@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(
    role_id: str,
    payload: TokenPayload = Depends(get_current_user_payload),
    db: sqlite3.Connection = Depends(get_db),
) -> dict:
    service = RoleService(db)
    service.delete_role(role_id=role_id, role_ids=payload.role_ids)
    return {"detail": "Role deleted"}
