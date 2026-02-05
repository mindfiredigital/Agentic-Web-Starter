import sqlite3
from typing import List


class ACLRepository:
    """Data access for role-component mappings."""

    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize the ACL repository."""
        self.db = db

    def get_component_ids_for_roles(self, role_ids: List[str]) -> List[str]:
        """Get the component IDs for the given roles."""

        if not role_ids:
            return []

        # Create placeholders for the role IDs.
        placeholders = ",".join("?" for _ in role_ids)
        
        # SQL query to get the component IDs for the given roles.
        COMPONENT_ID_ROLE_MAPPING_QUERY = f"""
            SELECT component_id
            FROM role_component_mapping
            WHERE role_id IN ({placeholders})
            """

        # Execute the SQL query and fetch the results.
        rows = self.db.execute(COMPONENT_ID_ROLE_MAPPING_QUERY, role_ids).fetchall()

        # Return the component IDs for the given roles.
        return [row[0] for row in rows]
