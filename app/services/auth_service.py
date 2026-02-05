import sqlite3

from app.exceptions import AuthenticationError, PermissionDeniedError
from app.repository.acl_repository import ACLRepository
from app.repository.component_repository import ComponentRepository
from app.repository.role_repository import RoleRepository
from app.repository.user_repository import UserRepository
from app.services.role_service import ROLE_COMPONENT_URI
from app.services.user_service import USER_COMPONENT_URI
from app.utils.auth_utils import auth_utils
from app.utils.jwt_utils import JWT_utils

class AuthService:
    """Authentication business logic."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.component_repo = ComponentRepository(db)
        self.acl_repo = ACLRepository(db)
        
    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_user_by_username(username)

        if not user or not auth_utils.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")

        roles = self.user_repo.get_roles_for_user(user.id)
        role_ids = [role.id for role in roles]
        return JWT_utils.create_access_token(user_id=user.id, role_ids=role_ids)

    def bootstrap_admin(self, username: str, email: str | None, password: str) -> bool:
        """Create the initial admin user if no users exist."""
        existing_users = self.user_repo.list_users()
        if existing_users:
            return False

        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            raise PermissionDeniedError("Username already exists")

        hashed_password = auth_utils.hash_password(password)
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

        users_component = self.component_repo.get_component_by_uri(USER_COMPONENT_URI)
        if not users_component:
            users_component = self.component_repo.create_component(
                name="users",
                component_uri=USER_COMPONENT_URI,
                created_by=user.id,
            )

        roles_component = self.component_repo.get_component_by_uri(ROLE_COMPONENT_URI)
        if not roles_component:
            roles_component = self.component_repo.create_component(
                name="roles",
                component_uri=ROLE_COMPONENT_URI,
                created_by=user.id,
            )

        self.user_repo.add_role_to_user(user.id, admin_role.id)
        self.acl_repo.add_component_to_role(admin_role.id, users_component.id)
        self.acl_repo.add_component_to_role(admin_role.id, roles_component.id)

        return True
