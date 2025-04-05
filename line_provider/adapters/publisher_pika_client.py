import pickle

import aio_pika
import aio_pika.abc
from core.settings import settings
from core.utils.loggers.logger import get_logger


class PikaPublisherClient:
    logger = get_logger("pika_client")

    def __init__(self) -> None:
        self.publish_queue_name = settings.rabbit.pika_publish_queue_name

    async def publish_to_queue(self, message: dict) -> None:
        message_body = aio_pika.Message(pickle.dumps(message))
        connection: aio_pika.abc.AbstractConnection = await aio_pika.connect_robust(
            host=settings.rabbit.host,
            port=settings.rabbit.port,
            login=settings.rabbit.login,
            password=settings.rabbit.password,
            heartbeat=60,
        )
        try:
            async with connection:
                channel: aio_pika.abc.AbstractChannel = await connection.channel()

                await channel.default_exchange.publish(
                    routing_key=self.publish_queue_name,
                    message=message_body,
                )
                self.logger.warning(f"'{message}' published to queue {self.publish_queue_name}")

        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
