import sqlite3
from datetime import datetime, timezone
from typing import Generator

from app.config.env_config import settings


def utc_now_iso() -> str:
    """Get the current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _connect() -> sqlite3.Connection:
    """Connect to the SQLite database."""
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Get a database connection."""
    db = _connect()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize the SQLite database."""
    db = _connect()
    try:
        cursor = db.cursor()

        # Create the users table.
        cursor.execute(
            """
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
        )

        # Create the roles table.
        cursor.execute(
            """
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
        )

        # Create the components table.
        cursor.execute(
            """
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
        )
        
        # Create the user_role_mapping table.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_role_mapping (
                user_id TEXT NOT NULL,
                role_id TEXT NOT NULL,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
            )
            """
        )
        # Create the role_component_mapping table.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS role_component_mapping (
                role_id TEXT NOT NULL,
                component_id TEXT NOT NULL,
                PRIMARY KEY (role_id, component_id),
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
                FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
            )
            """
        )
        # Commit the changes.
        db.commit()
    # Close the database connection.
    finally:
        db.close()


