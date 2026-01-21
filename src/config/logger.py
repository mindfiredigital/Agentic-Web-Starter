from datetime import datetime
import logging
import os
import sys

from src.config.settings import settings
from src.constants.app_constants import Environment

ENV = settings.ENV
LOG_DIR = Environment.LOG_DIR.value

# Create a custom logger
logger = logging.getLogger()  # Root logger instead of __name__ to catch all logs
logger.setLevel(logging.DEBUG)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if ENV == "dev" else logging.INFO)

# Create formatters and add it to handlers
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Simplified format for better CloudWatch integration
formatter = logging.Formatter(log_format)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

# Prevent logs from propagating to the root logger
logger.propagate = False

# Suppress verbose OpenAI and HTTP client logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("langchain.agents.agent_iterator").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)