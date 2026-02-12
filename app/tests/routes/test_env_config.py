import os
import importlib
from app.config import env_config

def test_reads_from_env(clear_env, set_env_vars):
    """Verify Settings loads values from environment."""
    importlib.reload(env_config)
    settings = env_config.Settings()

    assert settings.ENV == "dev"
    assert settings.PROJECT_NAME == "TestProj"
    assert settings.PROJECT_VERSION == "1.0.0"
    assert settings.ALLOWED_ORIGINS == ["http://localhost", "http://127.0.0.1"]
    assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 15


def test_paths_from_working_dir(clear_env, set_env_vars):
    """Verify paths are derived from WORKING_DIR."""
    importlib.reload(env_config)
    settings = env_config.Settings()

    expected_project_dir = os.path.join(str(set_env_vars), "TestProj")
    assert settings.WORKING_PROJECT_DIR == expected_project_dir
    assert settings.DB_PATH == os.path.join(str(set_env_vars), "sqlite_data", "app.db")
    assert settings.LOG_DIR == os.path.join(expected_project_dir, "logs")
    assert settings.UPLOAD_DIR == os.path.join(expected_project_dir, "static", "uploads")


def test_defaults_when_missing(clear_env):
    """Verify default values when env vars are absent."""
    importlib.reload(env_config)
    settings = env_config.Settings()

    assert settings.JWT_SECRET_KEY == "change-me"
    assert settings.JWT_ALGORITHM == "HS256"
    expected_expiry = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == expected_expiry
