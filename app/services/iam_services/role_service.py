from typing import List, Optional

import sqlite3

from app.config.log_config import logger
from app.exceptions import ConflictError, ForbiddenError, InternalError, NotFoundError
from app.repository.sql_repository import ACLRepository, ComponentRepository, RoleRepository
from app.constants.app_constants import ROUTE_CONSTANTS

ROLE_COMPONENT_URI = ROUTE_CONSTANTS.ROLE_COMPONENT_URI.value


class RoleService:
    """Role business logic with ACL enforcement."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.role_repo = RoleRepository(db)
        self.acl_repo = ACLRepository(db)
        self.component_repo = ComponentRepository(db)

    def _ensure_access(self, role_ids: List[str]) -> None:
        try:
            component = self.component_repo.get_component_by_uri(ROLE_COMPONENT_URI)
            if not component:
                raise NotFoundError("Component not registered")
            allowed_component_ids = self.acl_repo.get_component_ids_for_roles(role_ids)
            if component.id not in allowed_component_ids:
                raise ForbiddenError("Forbidden")
        except (NotFoundError, ForbiddenError):
            raise
        except sqlite3.Error as e:
            logger.exception("Database error in role service: %s", e)
            raise InternalError("Operation failed") from e

    def create_role(
        self,
        name: str,
        description: Optional[str],
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        try:
            existing_role = self.role_repo.get_role_by_name(name)
            if existing_role:
                raise ConflictError("Role already exists")
            return self.role_repo.create_role(
                name=name,
                description=description,
                created_by=current_user_id,
            )
        except (ConflictError, NotFoundError, ForbiddenError):
            raise
        except sqlite3.Error as e:
            logger.exception("Database error creating role: %s", e)
            raise InternalError("Create role failed") from e

    def get_role(self, role_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        try:
            role = self.role_repo.get_role_by_id(role_id)
            if not role:
                raise NotFoundError("Role not found")
            return role
        except NotFoundError:
            raise
        except sqlite3.Error as e:
            logger.exception("Database error fetching role: %s", e)
            raise InternalError("Get role failed") from e

    def list_roles(self, role_ids: List[str]):
        self._ensure_access(role_ids)
        try:
            return self.role_repo.list_roles()
        except sqlite3.Error as e:
            logger.exception("Database error listing roles: %s", e)
            raise InternalError("List roles failed") from e

    def update_role(
        self,
        role_id: str,
        name: Optional[str],
        description: Optional[str],
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        try:
            if name:
                existing_role = self.role_repo.get_role_by_name(name)
                if existing_role and existing_role.id != role_id:
                    raise ConflictError("Role already exists")
            role = self.role_repo.update_role(
                role_id=role_id,
                name=name,
                description=description,
                updated_by=current_user_id,
            )
            if not role:
                raise NotFoundError("Role not found")
            return role
        except (ConflictError, NotFoundError, ForbiddenError):
            raise
        except sqlite3.Error as e:
            logger.exception("Database error updating role: %s", e)
            raise InternalError("Update role failed") from e

    def delete_role(self, role_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        try:
            role = self.role_repo.delete_role(role_id)
            if not role:
                raise NotFoundError("Role not found")
            return role
        except NotFoundError:
            raise
        except sqlite3.Error as e:
            logger.exception("Database error deleting role: %s", e)
            raise InternalError("Delete role failed") from e

