from __future__ import annotations

import asyncio
from typing import Any

from app.config.env_config import settings
from app.config.log_config import logger
from app.services.core_services.ingestion_service import ingestion_service
from app.utils.core_utils.queue.rabbitmq_utils import consume_json


async def _handle_ingestion_message(payload: dict[str, Any], _message) -> None:
    saved_path = payload.get("saved_path")
    if not saved_path:
        logger.warning("Skipping message without saved_path: %s", payload)
        return

    logger.info("Worker ingesting saved_path=%s", saved_path)
    result = ingestion_service.index_file(str(saved_path))
    logger.info("Worker ingestion completed: %s", result)


async def main() -> None:
    if not settings.USE_RABBITMQ:
        logger.info("USE_RABBITMQ is false. Ingestion worker is disabled.")
        return

    queue_name = settings.RABBITMQ_INGEST_QUEUE
    logger.info("Starting ingestion worker. queue=%s", queue_name)
    await consume_json(queue_name, _handle_ingestion_message)


if __name__ == "__main__":
    asyncio.run(main())
