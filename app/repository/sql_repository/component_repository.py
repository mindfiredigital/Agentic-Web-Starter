import sqlite3
from typing import List, Optional

from app.models import Component
from app.repository.sql_repository.base_repository import BaseRepository


class ComponentRepository(BaseRepository[Component]):
    """Data access for components."""

    def __init__(self, db: sqlite3.Connection) -> None:
        super().__init__(db, "components", Component)

    def create_component(self, name: str, component_uri: str, created_by: Optional[str] = None) -> Component:
        """Create a new component."""
        return self.create(created_by=created_by, name=name, component_uri=component_uri)

    def get_component_by_id(self, component_id: str) -> Optional[Component]:
        """Get a component by ID."""
        return self.get_by_id(component_id)

    def get_component_by_uri(self, component_uri: str) -> Optional[Component]:
        """Get a component by URI."""
        return self.get_by_field("component_uri", component_uri)

    def get_component_by_name(self, name: str) -> Optional[Component]:
        """Get a component by name."""
        return self.get_by_field("name", name)

    def list_components(self) -> List[Component]:
        """List all components."""
        return self.list_all()
