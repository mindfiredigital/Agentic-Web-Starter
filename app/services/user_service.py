from typing import List, Optional

import sqlite3

from app.exceptions import DomainValidationError, NotFoundError, PermissionDeniedError
from app.repository.acl_repository import ACLRepository
from app.repository.component_repository import ComponentRepository
from app.repository.user_repository import UserRepository
from app.services.security import hash_password


USER_COMPONENT_URI = "/api/v1/users"


class UserService:
    """User business logic with ACL enforcement."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.acl_repo = ACLRepository(db)
        self.component_repo = ComponentRepository(db)

    def _ensure_access(self, role_ids: List[str]) -> None:
        component = self.component_repo.get_component_by_uri(USER_COMPONENT_URI)
        if not component:
            raise NotFoundError("Component not registered")

        allowed_component_ids = self.acl_repo.get_component_ids_for_roles(role_ids)
        if component.id not in allowed_component_ids:
            raise PermissionDeniedError("Forbidden")

    def create_user(
        self,
        username: str,
        email: Optional[str],
        password: str,
        current_user_id: str,
        role_ids: List[str],
    ):
        self._ensure_access(role_ids)
        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            raise DomainValidationError("Username already exists")
        hashed_password = hash_password(password)
        return self.user_repo.create_user(
            username=username,
            email=email,
            hashed_password=hashed_password,
            created_by=current_user_id,
        )

    def get_user(self, user_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def list_users(self, role_ids: List[str]):
        self._ensure_access(role_ids)
        return self.user_repo.list_users()

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
        if username:
            existing_user = self.user_repo.get_user_by_username(username)
            if existing_user and existing_user.id != user_id:
                raise DomainValidationError("Username already exists")
        hashed_password = hash_password(password) if password else None
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

    def delete_user(self, user_id: str, role_ids: List[str]):
        self._ensure_access(role_ids)
        user = self.user_repo.delete_user(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
