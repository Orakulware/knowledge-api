import logging
from abc import ABC, abstractmethod

from config import RabbitMQConfig, RedisConfig
from taskiq import AsyncBroker, AsyncResultBackend
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

logger = logging.getLogger(__name__)


class MediaRecordConsumer(ABC):
    @property
    @abstractmethod
    def broker(self) -> AsyncBroker:
        raise NotImplementedError

    @abstractmethod
    async def startup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError


class TaskiqAioPikaRedisMediaRecordConsumer(MediaRecordConsumer):
    """Media record consumer with Rabbit MQ broker and Redis backend"""

    def __init__(
        self,
        rabbitmq_config: RabbitMQConfig,
        redis_config: RedisConfig,
    ) -> None:
        self._rabbitmq_url = rabbitmq_config.url
        self._redis_url = redis_config.url

        self._result_backend: AsyncResultBackend = RedisAsyncResultBackend(
            redis_url=self._redis_url,
            keep_results=True,
            result_ex_time=86400,
        )

        self._broker: AsyncBroker = AioPikaBroker(
            url=self._rabbitmq_url,
        ).with_result_backend(
            self._result_backend,
        )

    @property
    def broker(self) -> AsyncBroker:
        return self._broker

    async def startup(self) -> None:
        logger.info("Starting up %s consumer", self.__class__.__name__)
        await self._broker.startup()

    async def shutdown(self) -> None:
        logger.info("Shuting down %s consumer", self.__class__.__name__)
        await self._broker.shutdown()
