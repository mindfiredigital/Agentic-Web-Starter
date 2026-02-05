import sqlite3
import uuid
from typing import List, Optional

from app.models import Role, User
from app.repository.sqlite_repository import utc_now_iso


class UserRepository:
    """Data access for users."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db

    def _row_to_user(self, row: sqlite3.Row | None) -> Optional[User]:
        """Convert a database row to a user."""
        if row is None:
            return None
        return User.model_validate(dict(row))

    def _rows_to_users(self, rows: List[sqlite3.Row]) -> List[User]:
        """Convert a list of database rows to a list of users."""
        return [self._row_to_user(row) for row in rows if row is not None]

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
        user_id = str(uuid.uuid4())
        
        # Get the current timestamp.
        now = utc_now_iso()
        
        # Execute the SQL query to create a new user.
        self.db.execute(
            """
            INSERT INTO users (id, username, email, hashed_password, created_at, created_by, updated_at, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, email, hashed_password, now, created_by, now, created_by),
        )
        # Commit the changes.
        self.db.commit()
        return self.get_user_by_id(user_id)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        
        # Execute the SQL query to get a user by ID.
        row = self.db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

        # Convert the database row to a user.
        return self._row_to_user(row)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        
        # Execute the SQL query to get a user by username.
        row = self.db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        # Convert the database row to a user.
        return self._row_to_user(row)

    def list_users(self) -> List[User]:
        """List all users."""
        
        # Execute the SQL query to list all users.
        rows = self.db.execute("SELECT * FROM users").fetchall()

        # Convert the database rows to a list of users.
        return self._rows_to_users(rows)

    def update_user(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        hashed_password: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Optional[User]:
        """Update a user by ID and return the updated user."""
        
        # Get the user by ID.
        user = self.get_user_by_id(user_id)
        if not user:
            # Return None if the user is not found.
            return None

        # Create the fields and values for the update.
        fields = []
        values = []
        if username is not None:
            fields.append("username = ?")
            values.append(username)
        if email is not None:
            fields.append("email = ?")
            values.append(email)
        if hashed_password is not None:
            fields.append("hashed_password = ?")
            values.append(hashed_password)
        if updated_by is not None:
            fields.append("updated_by = ?")
            values.append(updated_by)
        if fields:
            fields.append("updated_at = ?")
            values.append(utc_now_iso())
            values.append(user_id)
            # Execute the SQL query to update the user.
            self.db.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE id = ?",
                values,
            )
            # Commit the changes.
            self.db.commit()
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: str) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db.commit()
        return user

    def get_roles_for_user(self, user_id: str) -> List[Role]:
        rows = self.db.execute(
            """
            SELECT roles.*
            FROM roles
            JOIN user_role_mapping ON roles.id = user_role_mapping.role_id
            WHERE user_role_mapping.user_id = ?
            """,
            (user_id,),
        ).fetchall()
        return self._rows_to_roles(rows)
