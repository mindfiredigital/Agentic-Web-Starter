import sqlite3

from app.exceptions import AuthenticationError
from app.repository.user_repository import UserRepository
from app.services.security import verify_password
from app.utils.jwt_utils import create_access_token


class AuthService:
    """Authentication business logic."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")

        roles = self.user_repo.get_roles_for_user(user.id)
        role_ids = [role.id for role in roles]
        return create_access_token(user_id=user.id, role_ids=role_ids)
