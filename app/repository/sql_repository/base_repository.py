import sqlite3
import uuid
from typing import Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from app.utils.database import utc_now_iso

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations."""

    def __init__(self, db: sqlite3.Connection, table_name: str, model_class: Type[T]) -> None:
        """Initialize the base repository.
        
        Args:
            db: SQLite database connection
            table_name: Name of the database table
            model_class: Pydantic model class for type conversion
        """
        self.db = db
        self.table_name = table_name
        self.model_class = model_class

    def _row_to_model(self, row: sqlite3.Row | None) -> Optional[T]:
        """Convert a database row to a model instance.
        
        Args:
            row: Database row or None
            
        Returns:
            Model instance or None if row is None
        """
        if row is None:
            return None
        return self.model_class.model_validate(dict(row))

    def _rows_to_models(self, rows: List[sqlite3.Row]) -> List[T]:
        """Convert a list of database rows to a list of model instances.
        
        Args:
            rows: List of database rows
            
        Returns:
            List of model instances
        """
        return [self._row_to_model(row) for row in rows if row is not None]

    def get_by_id(self, id: str) -> Optional[T]:
        """Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        row = self.db.execute(query, (id,)).fetchone()
        return self._row_to_model(row)

    def get_by_field(self, field_name: str, field_value: str) -> Optional[T]:
        """Get a record by a specific field value.
        
        Args:
            field_name: Name of the field to query
            field_value: Value to search for
            
        Returns:
            Model instance or None if not found
        """
        query = f"SELECT * FROM {self.table_name} WHERE {field_name} = ?"
        row = self.db.execute(query, (field_value,)).fetchone()
        return self._row_to_model(row)

    def list_all(self) -> List[T]:
        """List all records.
        
        Returns:
            List of all model instances
        """
        query = f"SELECT * FROM {self.table_name}"
        rows = self.db.execute(query).fetchall()
        return self._rows_to_models(rows)

    def update(
        self,
        id: str,
        updated_by: Optional[str] = None,
        **fields
    ) -> Optional[T]:
        """Update a record by ID.
        
        Args:
            id: Record ID
            updated_by: User who is updating the record
            **fields: Fields to update (field_name=value)
            
        Returns:
            Updated model instance or None if not found
        """
        # Check if record exists
        record = self.get_by_id(id)
        if not record:
            return None

        # Build the update query
        update_fields = []
        values = []
        
        for field_name, field_value in fields.items():
            if field_value is not None:
                update_fields.append(f"{field_name} = ?")
                values.append(field_value)
        
        if updated_by is not None:
            update_fields.append("updated_by = ?")
            values.append(updated_by)
        
        if update_fields:
            update_fields.append("updated_at = ?")
            values.append(utc_now_iso())
            values.append(id)
            
            query = f"UPDATE {self.table_name} SET {', '.join(update_fields)} WHERE id = ?"
            self.db.execute(query, values)
            self.db.commit()
        
        return self.get_by_id(id)

    def delete(self, id: str) -> Optional[T]:
        """Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Deleted model instance or None if not found
        """
        record = self.get_by_id(id)
        if not record:
            return None
        
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        self.db.execute(query, (id,))
        self.db.commit()
        return record

    def create(
        self,
        created_by: Optional[str] = None,
        **fields
    ) -> T:
        """Create a new record.
        
        Args:
            created_by: User who is creating the record
            **fields: Fields for the new record (field_name=value)
            
        Returns:
            Created model instance
        """
        record_id = str(uuid.uuid4())
        current_time = utc_now_iso()
        
        # Build field names and values
        field_names = ["id", "created_at", "created_by", "updated_at", "updated_by"]
        field_values = [record_id, current_time, created_by, current_time, created_by]
        
        for field_name, field_value in fields.items():
            field_names.append(field_name)
            field_values.append(field_value)
        
        # Build the insert query
        placeholders = ", ".join("?" for _ in field_names)
        query = f"""
            INSERT INTO {self.table_name} ({', '.join(field_names)})
            VALUES ({placeholders})
        """
        
        self.db.execute(query, field_values)
        self.db.commit()
        return self.get_by_id(record_id)
