from __future__ import annotations

import json
from typing import Any, Awaitable, Callable

from aio_pika import DeliveryMode, Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection

from app.config.log_config import logger
from app.config.rabbitmq_config import rabbitmq_config

JsonDict = dict[str, Any]
MessageHandler = Callable[[JsonDict, AbstractIncomingMessage], Awaitable[None]]


class MessageQueueClient:
    """Client for publishing and consuming JSON messages from a message queue."""

    async def _connect(self) -> AbstractRobustConnection:
        """Establish a robust connection to the message broker.

        Returns:
            AbstractRobustConnection: A connected broker connection instance.
        """
        amqp_url = rabbitmq_config.get_amqp_url()
        return await connect_robust(amqp_url)

    async def publish_json(
        self, queue_name: str, payload: JsonDict, *, persistent: bool = True
    ) -> None:
        """Publish a JSON message to a durable queue (default exchange).

        Args:
            queue_name: Name of the queue to publish to.
            payload: JSON-serializable dict to publish as message body.
            persistent: If True, message survives broker restart. Defaults to True.
        """
        connection = await self._connect()
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(queue_name, durable=True)

            body = json.dumps(payload).encode("utf-8")
            message = Message(
                body=body,
                content_type="application/json",
                delivery_mode=(
                    DeliveryMode.PERSISTENT
                    if persistent
                    else DeliveryMode.NOT_PERSISTENT
                ),
            )

            await channel.default_exchange.publish(message, routing_key=queue_name)
            logger.info("Published message to queue=%s", queue_name)

    async def consume_json(
        self, queue_name: str, handler: MessageHandler, *, prefetch: int = 10
    ) -> None:
        """Consume JSON messages from a durable queue and call handler(payload, message).

        Args:
            queue_name: Name of the queue to consume from.
            handler: Async callback invoked with (payload_dict, message) for each message.
            prefetch: Maximum unacked messages per consumer. Defaults to 10.
        """
        connection = await self._connect()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=prefetch)
        queue = await channel.declare_queue(queue_name, durable=True)

        logger.info("Consuming message queue=%s", queue_name)
        try:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process(requeue=False):
                        payload = self._safe_json_loads(message.body)
                        await handler(payload, message)
        finally:
            await connection.close()

    @staticmethod
    def _safe_json_loads(body: bytes) -> JsonDict:
        """Decode bytes to JSON dict, with fallback for invalid payloads.

        Args:
            body: Raw message body bytes.

        Returns:
            Parsed dict, or {"_value": parsed} if parsed value is not dict,
            or {"_raw": decoded_str} if JSON decode fails.
        """
        try:
            parsed = json.loads(body.decode("utf-8"))
            if isinstance(parsed, dict):
                return parsed
            return {"_value": parsed}
        except Exception:
            return {"_raw": body.decode("utf-8", errors="replace")}
