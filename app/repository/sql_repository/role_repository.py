import sqlite3
from typing import List, Optional

from app.models import Role
from app.repository.sql_repository.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Data access for roles."""

    def __init__(self, db: sqlite3.Connection) -> None:
        """Initialize with database connection and roles table."""
        super().__init__(db, "roles", Role)

    def create_role(self, 
        name: str, 
        description: Optional[str] = None, 
        created_by: Optional[str] = None) -> Role:
        """Create a new role.

        Args:
            name: Role name.
            description: Optional description.
            created_by: Optional user ID of creator.

        Returns:
            Created Role instance.
        """
        return self.create(created_by=created_by, name=name, description=description)

    def get_role_by_id(self, role_id: str) -> Optional[Role]:
        """Get a role by ID.

        Args:
            role_id: Role identifier.

        Returns:
            Role instance or None.
        """
        return self.get_by_id(role_id)

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get a role by name.

        Args:
            name: Role name to search for.

        Returns:
            Role instance or None.
        """
        return self.get_by_field("name", name)

    def list_roles(self) -> List[Role]:
        """List all roles.

        Returns:
            List of Role instances.
        """
        return self.list_all()

    def update_role(
        self,
        role_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Optional[Role]:
        """Update a role.

        Args:
            role_id: Role identifier.
            name: Optional new name.
            description: Optional new description.
            updated_by: Optional user ID of updater.

        Returns:
            Updated Role instance or None if not found.
        """
        return self.update(role_id, updated_by=updated_by, name=name, description=description)

    def delete_role(self, role_id: str) -> Optional[Role]:
        """Delete a role.

        Args:
            role_id: Role identifier.

        Returns:
            Deleted Role instance or None if not found.
        """
        return self.delete(role_id)
