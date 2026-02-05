import sqlite3
import uuid
from typing import List, Optional

from app.models import Component
from app.repository.sqlite_repository import utc_now_iso


class ComponentRepository:
    """Data access for components."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db

    def _row_to_component(self, row: sqlite3.Row | None) -> Optional[Component]:
        """Convert a database row to a component."""
        if row is None:
            return None
        return Component.model_validate(dict(row))

    def _rows_to_components(self, rows: List[sqlite3.Row]) -> List[Component]:
        """Convert a list of database rows to a list of components."""
        return [self._row_to_component(row) for row in rows if row is not None]

    def create_component(
        self,
        name: str,
        component_uri: str,
        created_by: Optional[str] = None,
    ) -> Component:
        """Create a new component."""
        component_id = str(uuid.uuid4())

        # Get the current timestamp.
        
        now = utc_now_iso()
        # Execute the SQL query to create a new component.
        
        self.db.execute(
            """
            INSERT INTO components (id, name, component_uri, created_at, created_by, updated_at, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (component_id, name, component_uri, now, created_by, now, created_by),
        )
        self.db.commit()
        return self.get_component_by_id(component_id)

    def get_component_by_id(self, component_id: str) -> Optional[Component]:
        row = self.db.execute(
            "SELECT * FROM components WHERE id = ?",
            (component_id,),
        ).fetchone()
        return self._row_to_component(row)

    def get_component_by_uri(self, component_uri: str) -> Optional[Component]:
        row = self.db.execute(
            "SELECT * FROM components WHERE component_uri = ?",
            (component_uri,),
        ).fetchone()
        return self._row_to_component(row)

    def get_component_by_name(self, name: str) -> Optional[Component]:
        row = self.db.execute(
            "SELECT * FROM components WHERE name = ?",
            (name,),
        ).fetchone()
        return self._row_to_component(row)

    def list_components(self) -> List[Component]:
        rows = self.db.execute("SELECT * FROM components").fetchall()
        return self._rows_to_components(rows)
