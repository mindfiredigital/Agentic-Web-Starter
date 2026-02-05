import sqlite3
import uuid
from typing import List, Optional

from app.models import Role
from app.repository.sqlite_repository import utc_now_iso


class RoleRepository:
    """Data access for roles."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db

    def _row_to_role(self, row: sqlite3.Row | None) -> Optional[Role]:
        if row is None:
            return None
        return Role.model_validate(dict(row))

    def _rows_to_roles(self, rows: List[sqlite3.Row]) -> List[Role]:
        return [self._row_to_role(row) for row in rows if row is not None]

    def create_role(
        self,
        name: str,
        description: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Role:
        role_id = str(uuid.uuid4())
        now = utc_now_iso()
        self.db.execute(
            """
            INSERT INTO roles (id, name, description, created_at, created_by, updated_at, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (role_id, name, description, now, created_by, now, created_by),
        )
        self.db.commit()
        return self.get_role_by_id(role_id)

    def get_role_by_id(self, role_id: str) -> Optional[Role]:
        row = self.db.execute("SELECT * FROM roles WHERE id = ?", (role_id,)).fetchone()
        return self._row_to_role(row)

    def get_role_by_name(self, name: str) -> Optional[Role]:
        row = self.db.execute("SELECT * FROM roles WHERE name = ?", (name,)).fetchone()
        return self._row_to_role(row)

    def list_roles(self) -> List[Role]:
        rows = self.db.execute("SELECT * FROM roles").fetchall()
        return self._rows_to_roles(rows)

    def update_role(
        self,
        role_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Optional[Role]:
        role = self.get_role_by_id(role_id)
        if not role:
            return None
        fields = []
        values = []
        if name is not None:
            fields.append("name = ?")
            values.append(name)
        if description is not None:
            fields.append("description = ?")
            values.append(description)
        if updated_by is not None:
            fields.append("updated_by = ?")
            values.append(updated_by)
        if fields:
            fields.append("updated_at = ?")
            values.append(utc_now_iso())
            values.append(role_id)
            self.db.execute(
                f"UPDATE roles SET {', '.join(fields)} WHERE id = ?",
                values,
            )
            self.db.commit()
        return self.get_role_by_id(role_id)

    def delete_role(self, role_id: str) -> Optional[Role]:
        role = self.get_role_by_id(role_id)
        if not role:
            return None
        self.db.execute("DELETE FROM roles WHERE id = ?", (role_id,))
        self.db.commit()
        return role
