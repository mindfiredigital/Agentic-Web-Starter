from __future__ import annotations

import asyncio
from typing import Any

from app.config.env_config import settings
from app.config.log_config import logger
from app.tools.indexer_tool import IndexerTool
from app.utils.core_utils.queue.rabbitmq_utils import consume_json


async def _handle_ingestion_message(payload: dict[str, Any], _message) -> None:
    """Process a single ingestion message from RabbitMQ.

    Args:
        payload: Message body; must contain "saved_path" key.
        _message: Raw aio_pika message (unused).
    """
    saved_path = payload.get("saved_path")
    if not saved_path:
        logger.warning("Skipping message without saved_path: %s", payload)
        return

    logger.info("Worker ingesting saved_path=%s", saved_path)
    index_tool = IndexerTool(filepath=str(saved_path))
    result = index_tool._run()
    logger.info("Worker ingestion completed: %s", result)


async def main() -> None:
    """Start the ingestion worker consuming from the configured queue."""
    queue_name = settings.RABBITMQ_INGEST_QUEUE
    logger.info("Starting ingestion worker. queue=%s", queue_name)
    await consume_json(queue_name, _handle_ingestion_message)


if __name__ == "__main__":
    asyncio.run(main())
