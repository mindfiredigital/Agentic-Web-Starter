import json
import logging
from datetime import datetime, timezone

from app.config.env_config import settings

ENV = settings.ENV
LOG_LEVEL = logging.DEBUG if ENV == "dev" else logging.INFO


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            JSON-encoded string representation of the log entry.
        """
        log_entry = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "env": ENV,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            log_entry["stack"] = self.formatStack(record.stack_info)

        return json.dumps(log_entry, ensure_ascii=True)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=LOG_LEVEL, handlers=[handler])
logger = logging.getLogger("app")

# Suppress verbose OpenAI and HTTP client logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("langchain.agents.agent_iterator").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers.SentenceTransformer").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("tokenizers").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.WARNING)
