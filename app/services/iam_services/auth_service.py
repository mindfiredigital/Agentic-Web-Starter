import sqlite3

from app.config.log_config import logger
from app.exceptions import ConflictError, InternalError, UnauthorizedError
from app.repository.sql_repository import (
    ACLRepository,
    ComponentRepository,
    RoleRepository,
    UserRepository,
)
from app.services.iam_services.role_service import ROLE_COMPONENT_URI
from app.services.iam_services.user_service import USER_COMPONENT_URI
from app.utils.iam_utils import JWT_utils, auth_utils


class AuthService:
    """Authentication business logic."""

    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize AuthService with database connection.

        Args:
            db: Active SQLite connection.
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.component_repo = ComponentRepository(db)
        self.acl_repo = ACLRepository(db)

    def login(self, username: str, password: str) -> str:
        """Authenticate user and return JWT access token.

        Args:
            username: User's username.
            password: Plain text password.

        Returns:
            JWT access token string.

        Raises:
            UnauthorizedError: If credentials are invalid.
            InternalError: If database operations fail.
        """
        try:
            user = self.user_repo.get_user_by_username(username)
        except sqlite3.Error as e:
            logger.exception("Database error during login: %s", e)
            raise InternalError("Authentication failed") from e

        if not user or not auth_utils.verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")

        try:
            roles = self.user_repo.get_roles_for_user(user.id)
            role_ids = [role.id for role in roles]
            return JWT_utils.create_access_token(user_id=user.id, role_ids=role_ids)
        except sqlite3.Error as e:
            logger.exception("Database error during login: %s", e)
            raise InternalError("Authentication failed") from e

    def bootstrap_admin(self, username: str, email: str | None, password: str) -> bool:
        """Create the initial admin user if no users exist.

        Args:
            username: Admin username.
            email: Admin email (optional).
            password: Admin password.

        Returns:
            True if admin was created, False if users already exist.

        Raises:
            ConflictError: If username already exists.
            InternalError: If bootstrap fails.
        """
        try:
            existing_users = self.user_repo.list_users()
        except sqlite3.Error as e:
            logger.exception("Database error during bootstrap: %s", e)
            raise InternalError("Bootstrap failed") from e

        if existing_users:
            return False

        try:
            existing_user = self.user_repo.get_user_by_username(username)
        except sqlite3.Error as e:
            logger.exception("Database error during bootstrap: %s", e)
            raise InternalError("Bootstrap failed") from e

        if existing_user:
            raise ConflictError("Username already exists")

        hashed_password = auth_utils.hash_password(password)
        try:
            user = self.user_repo.create_user(
                username=username,
                email=email,
                hashed_password=hashed_password,
            )

            admin_role = self.role_repo.get_role_by_name("admin")
            if not admin_role:
                admin_role = self.role_repo.create_role(
                    name="admin",
                    description="Initial administrator role",
                    created_by=user.id,
                )

            users_component = self.component_repo.get_component_by_uri(
                USER_COMPONENT_URI
            )
            if not users_component:
                users_component = self.component_repo.create_component(
                    name="users",
                    component_uri=USER_COMPONENT_URI,
                    created_by=user.id,
                )

            roles_component = self.component_repo.get_component_by_uri(
                ROLE_COMPONENT_URI
            )
            if not roles_component:
                roles_component = self.component_repo.create_component(
                    name="roles",
                    component_uri=ROLE_COMPONENT_URI,
                    created_by=user.id,
                )

            self.user_repo.add_role_to_user(user.id, admin_role.id)
            self.acl_repo.add_component_to_role(admin_role.id, users_component.id)
            self.acl_repo.add_component_to_role(admin_role.id, roles_component.id)
        except sqlite3.Error as e:
            logger.exception("Database error during bootstrap: %s", e)
            raise InternalError("Bootstrap failed") from e

        return True
