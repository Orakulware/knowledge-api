from config import RabbitMQConfig, RedisConfig
from taskiq import AsyncBroker, AsyncResultBackend
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

result_backend: AsyncResultBackend = RedisAsyncResultBackend(
    redis_url=RedisConfig.from_env().url,
    keep_results=True,
    result_ex_time=86400,
)

broker: AsyncBroker = AioPikaBroker(
    url=RabbitMQConfig.from_env().url,
).with_result_backend(
    result_backend,
)
