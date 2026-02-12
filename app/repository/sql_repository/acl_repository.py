import sqlite3
from typing import List


class ACLRepository:
    """Data access for role-component mappings."""

    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize the ACL repository.

        Args:
            db: Active SQLite connection.
        """
        self.db = db

    def get_component_ids_for_roles(self, role_ids: List[str]) -> List[str]:
        """Get the component IDs for the given roles.

        Args:
            role_ids: List of role identifiers.

        Returns:
            List of component IDs the roles can access.
        """

        if not role_ids:
            return []

        placeholders = ",".join("?" for _ in role_ids)

        ROLE_COMPONENT_MAPPING_QUERY = f"""
            SELECT component_id
            FROM role_component_mapping
            WHERE role_id IN ({placeholders})
            """
        rows = self.db.execute(ROLE_COMPONENT_MAPPING_QUERY, role_ids).fetchall()
        return [row[0] for row in rows]

    def add_component_to_role(self, role_id: str, component_id: str) -> None:
        """Map a role to a component.

        Args:
            role_id: Role identifier.
            component_id: Component identifier.
        """
        ROLE_COMPONENT_MAPPING_INSERT_QUERY = """
            INSERT OR IGNORE INTO role_component_mapping (role_id, component_id)
            VALUES (?, ?)
            """
        self.db.execute(ROLE_COMPONENT_MAPPING_INSERT_QUERY, (role_id, component_id))
        self.db.commit()
