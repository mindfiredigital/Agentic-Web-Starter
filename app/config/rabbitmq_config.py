from __future__ import annotations

from urllib.parse import quote

from app.config.env_config import settings


class RabbitMQConfig:
    """Provide RabbitMQ connection details and helpers."""

    def __init__(self) -> None:
        """Initialize RabbitMQ config from environment settings."""
        self.host: str = settings.RABBITMQ_HOST
        self.port: int = int(settings.RABBITMQ_PORT)
        self.username: str = settings.RABBITMQ_USERNAME
        self.password: str = settings.RABBITMQ_PASSWORD
        self.vhost: str = settings.RABBITMQ_VHOST or "/"
        self.amqp_url_override: str | None = settings.RABBITMQ_AMQP_URL

    def get_amqp_url(self) -> str:
        """Return AMQP URL string for aio-pika / AMQP clients.

        Returns:
            Full AMQP connection URL including host, port, credentials, and vhost.
        """
        if self.amqp_url_override:
            return self.amqp_url_override

        # In AMQP URLs, the vhost path segment should be URL-encoded ("/" -> "%2F").
        encoded_vhost = quote(self.vhost, safe="")
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/{encoded_vhost}"


rabbitmq_config = RabbitMQConfig()
