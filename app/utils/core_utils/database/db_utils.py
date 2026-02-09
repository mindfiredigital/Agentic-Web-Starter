import sqlite3
from datetime import datetime, timezone
from typing import Generator, Optional

from app.config.env_config import settings
from app.config.log_config import logger
from app.exceptions import InternalError


def utc_now_iso() -> str:
    """Get the current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


class SQLiteDatabase:
    """SQLite database manager with connection pooling and schema initialization."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database manager.

        Args:
            db_path: Optional path to the database file. Defaults to settings.DB_PATH.
        """
        self.db_path = db_path or settings.DB_PATH
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Create and return a new database connection.

        Returns:
            SQLite database connection with Row factory.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connections.

        Yields:
            SQLite database connection that auto-closes.
        """
        db = self.connect()
        try:
            yield db
        finally:
            db.close()

    def initialize_schema(self) -> None:
        """Initialize the database schema with all required tables.

        Raises:
            InternalError: If database initialization fails.
        """
        try:
            db = self.connect()
        except sqlite3.Error as e:
            logger.exception("Database connection failed: %s", e)
            raise InternalError("Database initialization failed") from e

        try:
            self._create_users_table(db)
            self._create_roles_table(db)
            self._create_components_table(db)
            self._create_user_role_mapping_table(db)
            self._create_role_component_mapping_table(db)

            db.commit()
            logger.info("Database schema initialized successfully")

        except sqlite3.Error as e:
            logger.exception("Database schema creation failed: %s", e)
            raise InternalError("Database initialization failed") from e
        finally:
            db.close()

    def _create_users_table(self, db: sqlite3.Connection) -> None:
        """Create the users table."""
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                hashed_password TEXT NOT NULL,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT
            )
        """
        db.execute(query)

    def _create_roles_table(self, db: sqlite3.Connection) -> None:
        """Create the roles table."""
        query = """
            CREATE TABLE IF NOT EXISTS roles (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT
            )
        """
        db.execute(query)

    def _create_components_table(self, db: sqlite3.Connection) -> None:
        """Create the components table."""
        query = """
            CREATE TABLE IF NOT EXISTS components (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                component_uri TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT
            )
        """
        db.execute(query)

    def _create_user_role_mapping_table(self, db: sqlite3.Connection) -> None:
        """Create the user_role_mapping table."""
        query = """
            CREATE TABLE IF NOT EXISTS user_role_mapping (
                user_id TEXT NOT NULL,
                role_id TEXT NOT NULL,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
            )
        """
        db.execute(query)

    def _create_role_component_mapping_table(self, db: sqlite3.Connection) -> None:
        """Create the role_component_mapping table."""
        query = """
            CREATE TABLE IF NOT EXISTS role_component_mapping (
                role_id TEXT NOT NULL,
                component_id TEXT NOT NULL,
                PRIMARY KEY (role_id, component_id),
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
                FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
            )
        """
        db.execute(query)

    def execute_query(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False,
    ):
        """Execute a query with automatic connection management.

        Args:
            query: SQL query to execute.
            params: Query parameters.
            fetch_one: Whether to fetch a single row.
            fetch_all: Whether to fetch all rows.

        Returns:
            Query result based on fetch parameters.
        """
        with self.get_connection() as db:
            cursor = db.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            db.commit()
            return cursor


sqlite_db = SQLiteDatabase()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Get a database connection (backward compatibility)."""
    yield from sqlite_db.get_connection()


def init_db() -> None:
    """Initialize the database schema (backward compatibility)."""
    sqlite_db.initialize_schema()

