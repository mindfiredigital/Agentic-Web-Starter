import glob
import json
import logging
import os
from datetime import datetime, timezone
from logging.handlers import BaseRotatingHandler

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


class DailyFileHandler(BaseRotatingHandler):
    """Writes logs to YYYY-MM-DD.log, rotating into a new file each UTC day.

    Files are named by date (e.g. 2026-04-15.log). Old files beyond
    `backup_count` days are removed automatically on rollover.
    """

    def __init__(self, log_dir: str, backup_count: int = 30, encoding: str = "utf-8"):
        self.log_dir = log_dir
        self.backup_count = backup_count
        self._current_date = self._today()
        filename = os.path.join(log_dir, f"{self._current_date}.log")
        super().__init__(filename, mode="a", encoding=encoding, delay=False)

    @staticmethod
    def _today() -> str:
        return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    def shouldRollover(self, record: logging.LogRecord) -> bool:  # type: ignore[override]
        return self._today() != self._current_date

    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None  # type: ignore[assignment]

        self._current_date = self._today()
        self.baseFilename = os.path.join(self.log_dir, f"{self._current_date}.log")
        self.stream = self._open()
        self._remove_old_logs()

    def _remove_old_logs(self) -> None:
        logs = sorted(glob.glob(os.path.join(self.log_dir, "????-??-??.log")))
        while len(logs) > self.backup_count:
            os.remove(logs.pop(0))


# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())

handlers: list[logging.Handler] = [console_handler]

# File handler — writes to LOG_DIR/YYYY-MM-DD.log, rotates at UTC midnight
if settings.LOG_DIR:
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    file_handler = DailyFileHandler(settings.LOG_DIR, backup_count=30)
    file_handler.setFormatter(JsonFormatter())
    handlers.append(file_handler)

logging.basicConfig(level=LOG_LEVEL, handlers=handlers)
logger = logging.getLogger("app")

# Suppress verbose third-party logs
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
