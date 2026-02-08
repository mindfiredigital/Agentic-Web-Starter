import sqlite3
from typing import List, Optional

from app.models import Role, User
from app.repository.sql_repository.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """Data access for users."""

    def __init__(self, db: sqlite3.Connection) -> None:
        super().__init__(db, "users", User)

    def _row_to_role(self, row: sqlite3.Row | None) -> Optional[Role]:
        """Convert a database row to a role."""
        if row is None:
            return None
        return Role.model_validate(dict(row))

    def _rows_to_roles(self, rows: List[sqlite3.Row]) -> List[Role]:
        """Convert a list of database rows to a list of roles."""
        return [self._row_to_role(row) for row in rows if row is not None]

    def create_user(
        self,
        username: str,
        email: Optional[str],
        hashed_password: str,
        created_by: Optional[str] = None,
    ) -> User:
        """Create a new user."""
        return self.create(
            created_by=created_by,
            username=username,
            email=email,
            hashed_password=hashed_password
        )

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.get_by_field("username", username)

    def list_users(self) -> List[User]:
        """List all users."""
        return self.list_all()

    def add_role_to_user(self, user_id: str, role_id: str) -> None:
        """Assign a role to a user."""
        USER_ROLE_MAPPING_INSERT_QUERY = """
            INSERT OR IGNORE INTO user_role_mapping (user_id, role_id)
            VALUES (?, ?)
            """
        self.db.execute(USER_ROLE_MAPPING_INSERT_QUERY, (user_id, role_id))
        self.db.commit()

    def update_user(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        hashed_password: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Optional[User]:
        """Update a user by ID and return the updated user."""
        return self.update(
            user_id,
            updated_by=updated_by,
            username=username,
            email=email,
            hashed_password=hashed_password
        )

    def delete_user(self, user_id: str) -> Optional[User]:
        """Delete a user."""
        return self.delete(user_id)

    def get_roles_for_user(self, user_id: str) -> List[Role]:
        """Get all roles assigned to a user."""
        GET_ROLES_FOR_USER_QUERY = """
            SELECT roles.*
            FROM roles
            JOIN user_role_mapping ON roles.id = user_role_mapping.role_id
            WHERE user_role_mapping.user_id = ?
            """
        rows = self.db.execute(GET_ROLES_FOR_USER_QUERY, (user_id,)).fetchall()
        return self._rows_to_roles(rows)
