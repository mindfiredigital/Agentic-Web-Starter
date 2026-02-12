"""Pytest fixtures for application tests."""

import importlib

import pytest
from fastapi.testclient import TestClient


ENV_VARS = [
    "ENV",
    "PROJECT_NAME",
    "PROJECT_VERSION",
    "PROJECT_DESCRIPTION",
    "ALLOWED_ORIGINS",
    "BASE_PATH",
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "JWT_SECRET_KEY",
    "JWT_ALGORITHM",
    "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    "ADMIN_USERNAME",
    "ADMIN_EMAIL",
    "ADMIN_PASSWORD",
    "WORKING_DIR",
    "HF_HOME",
    "COLLECTION_NAME",
    "QDRANT_HOST",
    "QDRANT_PORT",
    "QDRANT_PROTOCOL",
    "REDIS_HOST",
    "REDIS_PORT",
    "REDIS_PROTOCOL",
    "REDIS_DB",
]


@pytest.fixture
def clear_env(monkeypatch):
    """Remove standard env vars so tests start with clean state."""
    for var in ENV_VARS:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def set_env_vars(monkeypatch, tmp_path):
    """Set required env vars for test runs.

    Args:
        monkeypatch: Pytest monkeypatch.
        tmp_path: Temporary directory path.

    Returns:
        tmp_path for use by dependent fixtures.
    """
    monkeypatch.setenv("ENV", "dev")
    monkeypatch.setenv("PROJECT_NAME", "TestProj")
    monkeypatch.setenv("PROJECT_VERSION", "1.0.0")
    monkeypatch.setenv("PROJECT_DESCRIPTION", "Test project")
    monkeypatch.setenv("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1")
    monkeypatch.setenv("BASE_PATH", "")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("GEMINI_API_KEY", "gm-test")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin-password")
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture
def client(clear_env, set_env_vars, monkeypatch):
    """Provide a TestClient for the FastAPI app with mocked DB init and bootstrap."""
    from app.config import env_config, log_config

    importlib.reload(env_config)
    importlib.reload(log_config)

    from app import starter as starter_module

    monkeypatch.setattr(starter_module, "init_db", lambda: None)
    monkeypatch.setattr(starter_module, "_bootstrap_admin_user", lambda: None)

    app = starter_module.start_application()
    yield TestClient(app)
