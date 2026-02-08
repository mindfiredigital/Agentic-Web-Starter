from typing import List, Optional

import sqlite3

from app.config.log_config import logger
from app.exceptions import ConflictError, ForbiddenError, InternalError, NotFoundError
from app.repository.acl_repository import ACLRepository
from app.repository.component_repository import ComponentRepository
from app.repository.role_repository import RoleRepository
from app.repository.user_repository import UserRepository
from app.utils.auth_utils import auth_utils


USER_COMPONENT_URI = "/api/v1/users"


class UserService:
    """User business logic with ACL enforcement."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.acl_repo = ACLRepository(db)
        self.component_repo = ComponentRepository(db)

    def _ensure_access(self, role_ids: List[str]) -> None:
        try:
            component = self.component_repo.get_component_by_uri(USER_COMPONENT_URI)
            if not component:
                raise NotFoundError("Component not registered")
            allowed_component_ids = self.acl_repo.get_component_ids_for_roles(role_ids)
            if component.id not in allowed_component_ids:
                raise ForbiddenError("Forbidden")
        except (NotFoundError, ForbiddenError):
            raise
        except sqlite3.Error as e:
            logger.exception("Database error in user service: %s", e)
            raise InternalError("Operation failed") from e

    def create_user(
        self,
        username: str,
        email: Optional[str],
        password: str,
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        try:
            existing_user = self.user_repo.get_user_by_username(username)
            if existing_user:
                raise ConflictError("Username already exists")
            hashed_password = auth_utils.hash_password(password)
            user = self.user_repo.create_user(
                username=username,
                email=email,
                hashed_password=hashed_password,
                created_by=current_user_id,
            )
            default_role = self.role_repo.get_role_by_name("member")
            if not default_role:
                default_role = self.role_repo.create_role(
                    name="member",
                    description="Default member role",
                    created_by=current_user_id,
                )
            self.user_repo.add_role_to_user(user.id, default_role.id)
            return user
        except (ConflictError, NotFoundError, ForbiddenError):
            raise
        except sqlite3.Error as e:
            logger.exception("Database error creating user: %s", e)
            raise InternalError("Create user failed") from e

    def get_user(self, user_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            return user
        except NotFoundError:
            raise
        except sqlite3.Error as e:
            logger.exception("Database error fetching user: %s", e)
            raise InternalError("Get user failed") from e

    def list_users(self, role_ids: List[str]):
        self._ensure_access(role_ids)
        try:
            return self.user_repo.list_users()
        except sqlite3.Error as e:
            logger.exception("Database error listing users: %s", e)
            raise InternalError("List users failed") from e

    def update_user(
        self,
        user_id: str,
        username: Optional[str],
        email: Optional[str],
        password: Optional[str],
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        try:
            if username:
                existing_user = self.user_repo.get_user_by_username(username)
                if existing_user and existing_user.id != user_id:
                    raise ConflictError("Username already exists")
            hashed_password = auth_utils.hash_password(password) if password else None
            user = self.user_repo.update_user(
                user_id=user_id,
                username=username,
                email=email,
                hashed_password=hashed_password,
                updated_by=current_user_id,
            )
            if not user:
                raise NotFoundError("User not found")
            return user
        except (ConflictError, NotFoundError, ForbiddenError):
            raise
        except sqlite3.Error as e:
            logger.exception("Database error updating user: %s", e)
            raise InternalError("Update user failed") from e

    def delete_user(self, user_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        try:
            user = self.user_repo.delete_user(user_id)
            if not user:
                raise NotFoundError("User not found")
            return user
        except NotFoundError:
            raise
        except sqlite3.Error as e:
            logger.exception("Database error deleting user: %s", e)
            raise InternalError("Delete user failed") from e
