from typing import List, Optional

import sqlite3

from app.exceptions import DomainValidationError, NotFoundError, PermissionDeniedError
from app.repository.acl_repository import ACLRepository
from app.repository.component_repository import ComponentRepository
from app.repository.role_repository import RoleRepository


ROLE_COMPONENT_URI = "/api/v1/roles"


class RoleService:
    """Role business logic with ACL enforcement."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.role_repo = RoleRepository(db)
        self.acl_repo = ACLRepository(db)
        self.component_repo = ComponentRepository(db)

    def _ensure_access(self, role_ids: List[str]) -> None:
        component = self.component_repo.get_component_by_uri(ROLE_COMPONENT_URI)
        if not component:
            raise NotFoundError("Component not registered")

        allowed_component_ids = self.acl_repo.get_component_ids_for_roles(role_ids)
        if component.id not in allowed_component_ids:
            raise PermissionDeniedError("Forbidden")

    def create_role(
        self,
        name: str,
        description: Optional[str],
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        existing_role = self.role_repo.get_role_by_name(name)
        if existing_role:
            raise DomainValidationError("Role already exists")
        return self.role_repo.create_role(
            name=name,
            description=description,
            created_by=current_user_id,
        )

    def get_role(self, role_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        role = self.role_repo.get_role_by_id(role_id)
        if not role:
            raise NotFoundError("Role not found")
        return role

    def list_roles(self, role_ids: List[str]):
        self._ensure_access(role_ids)
        return self.role_repo.list_roles()

    def update_role(
        self,
        role_id: str,
        name: Optional[str],
        description: Optional[str],
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        if name:
            existing_role = self.role_repo.get_role_by_name(name)
            if existing_role and existing_role.id != role_id:
                raise DomainValidationError("Role already exists")
        role = self.role_repo.update_role(
            role_id=role_id,
            name=name,
            description=description,
            updated_by=current_user_id,
        )
        if not role:
            raise NotFoundError("Role not found")
        return role

    def delete_role(self, role_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        role = self.role_repo.delete_role(role_id)
        if not role:
            raise NotFoundError("Role not found")
        return role
