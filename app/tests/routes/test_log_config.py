import json
import logging
import importlib

from app.config import env_config, log_config


def test_json_formatter_includes_env(clear_env, set_env_vars):
    """Verify JsonFormatter outputs JSON with message, level, and env."""
    importlib.reload(env_config)
    importlib.reload(log_config)

    formatter = log_config.JsonFormatter()
    record = logging.LogRecord(
        name="app",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log",
        args=(),
        exc_info=None,
    )
    payload = json.loads(formatter.format(record))

    assert payload["message"] == "Test log"
    assert payload["level"] == "INFO"
    assert payload["env"] == "dev"


def test_log_level_from_env(clear_env, set_env_vars):
    """Verify LOG_LEVEL is DEBUG when ENV is dev."""
    importlib.reload(env_config)
    importlib.reload(log_config)

    assert log_config.LOG_LEVEL == logging.DEBUG
