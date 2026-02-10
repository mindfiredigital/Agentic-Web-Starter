from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Optional

from aio_pika import DeliveryMode, Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection

from app.config.log_config import logger
from app.config.rabbitmq_config import rabbitmq_config


JsonDict = dict[str, Any]
MessageHandler = Callable[[JsonDict, AbstractIncomingMessage], Awaitable[None]]


async def _connect() -> AbstractRobustConnection:
    amqp_url = rabbitmq_config.get_amqp_url()
    return await connect_robust(amqp_url)


async def publish_json(queue_name: str, payload: JsonDict, *, persistent: bool = True) -> None:
    """Publish a JSON message to a durable queue (default exchange)."""
    connection = await _connect()
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, durable=True)

        body = json.dumps(payload).encode("utf-8")
        message = Message(
            body=body,
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT if persistent else DeliveryMode.NOT_PERSISTENT,
        )

        await channel.default_exchange.publish(message, routing_key=queue_name)
        logger.info("Published message to queue=%s", queue_name)


async def consume_json(queue_name: str, handler: MessageHandler, *, prefetch: int = 10) -> None:
    """Consume JSON messages from a durable queue and call handler(payload, message)."""
    connection = await _connect()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=prefetch)
    queue = await channel.declare_queue(queue_name, durable=True)

    logger.info("Consuming RabbitMQ queue=%s", queue_name)
    try:
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(requeue=False):
                    payload = _safe_json_loads(message.body)
                    await handler(payload, message)
    finally:
        await connection.close()


def _safe_json_loads(body: bytes) -> JsonDict:
    try:
        parsed = json.loads(body.decode("utf-8"))
        if isinstance(parsed, dict):
            return parsed
        return {"_value": parsed}
    except Exception:
        # Keep the raw payload for debugging if decoding fails.
        return {"_raw": body.decode("utf-8", errors="replace")}

