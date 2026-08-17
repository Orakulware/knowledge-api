from dependency_injector import containers, providers
from media_record.application import PostMedia, PostMediaRecord
from media_record.infrastructure.consumer.consumer import (
    TaskiqAioPikaRedisMediaRecordConsumer,
)
from media_record.infrastructure.infrastructure import (
    SQLAlchemyMediaRepository,
    SQLAlchemyRecordRepository,
)
from shared.transaction_manager import SQLAlchemySessionTransactionManager


class MediaRecordInfrastructureProvider(containers.DeclarativeContainer):
    session = providers.Dependency()
    rabbitmq_config = providers.Dependency()
    redis_config = providers.Dependency()

    media_record_repository = providers.Factory(
        SQLAlchemyRecordRepository,
        session=session,
    )
    media_repository = providers.Factory(
        SQLAlchemyMediaRepository,
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
    media_repository = providers.Dependency()
    transaction_manager = providers.Dependency()

    post_media_record = providers.Factory(
        PostMediaRecord,
        caller_identity=caller_identity,
        transaction_manager=transaction_manager,
        media_record_repository=media_record_repository,
    )
    post_media = providers.Factory(
        PostMedia,
        transaction_manager=transaction_manager,
        media_repository=media_repository,
    )
