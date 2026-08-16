from dependency_injector import containers, providers
from media_record.application import PostMediaRecord
from media_record.infrastructure.consumer.consumer import (
    TaskiqAioPikaRedisMediaRecordConsumer,
)
from media_record.infrastructure.infrastructure import SQLAlchemyRecordRepository
from shared.transaction_manager import SQLAlchemySessionTransactionManager


class MediaRecordInfrastructureProvider(containers.DeclarativeContainer):
    session = providers.Dependency()
    rabbitmq_config = providers.Dependency()
    redis_config = providers.Dependency()

    media_record_repository = providers.Factory(
        SQLAlchemyRecordRepository,
        session=session,
    )
    transaction_manager = providers.Factory(
        SQLAlchemySessionTransactionManager,
        session=session,
    )
    media_record_consumer = providers.Singleton(
        TaskiqAioPikaRedisMediaRecordConsumer,
        rabbitmq_config=rabbitmq_config,
        redis_config=redis_config,
    )


class MediaRecordApplicationProvider(containers.DeclarativeContainer):
    caller_identity = providers.Dependency()
    media_record_repository = providers.Dependency()
    transaction_manager = providers.Dependency()

    post_media_record = providers.Factory(
        PostMediaRecord,
        caller_identity=caller_identity,
        transaction_manager=transaction_manager,
        media_record_repository=media_record_repository,
    )
