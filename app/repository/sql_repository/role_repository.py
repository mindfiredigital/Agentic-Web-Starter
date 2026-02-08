import sqlite3
from typing import List, Optional

from app.models import Role
from app.repository.sql_repository.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Data access for roles."""

    def __init__(self, db: sqlite3.Connection) -> None:
        super().__init__(db, "roles", Role)

    def create_role(self, 
        name: str, 
        description: Optional[str] = None, 
        created_by: Optional[str] = None) -> Role:
        """Create a new role."""
        return self.create(created_by=created_by, name=name, description=description)

    def get_role_by_id(self, role_id: str) -> Optional[Role]:
        """Get a role by ID."""
        return self.get_by_id(role_id)

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get a role by name."""
        return self.get_by_field("name", name)

    def list_roles(self) -> List[Role]:
        """List all roles."""
        return self.list_all()

    def update_role(
        self,
        role_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Optional[Role]:
        """Update a role."""
        return self.update(role_id, updated_by=updated_by, name=name, description=description)

    def delete_role(self, role_id: str) -> Optional[Role]:
        """Delete a role."""
        return self.delete(role_id)
