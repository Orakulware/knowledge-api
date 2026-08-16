from collections.abc import AsyncGenerator

from dependencies import get_caller_identity
from dependency_injector import containers, providers
from setup.media_record_providers import (
    MediaRecordApplicationProvider,
    MediaRecordInfrastructureProvider,
)
from setup.providers import ApplicationConfigProvider
from shared.database import SQLAlchemyDatabase
from sqlalchemy.ext.asyncio import AsyncSession


async def _db_session(database: SQLAlchemyDatabase) -> AsyncGenerator[AsyncSession]:
    async with database.get_session() as session:
        yield session


class Container(containers.DeclarativeContainer):
    config = providers.Container(ApplicationConfigProvider)
    database = providers.Singleton(SQLAlchemyDatabase, config=config.postgres)
    db_session = providers.ContextLocalResource(_db_session, database=database)

    caller_identity = providers.Factory(get_caller_identity)

    media_record_infrastructure = providers.Container(
        MediaRecordInfrastructureProvider,
        session=db_session,
        rabbitmq_config=config.rabbitmq,
        redis_config=config.redis,
    )
    media_record_application = providers.Container(
        MediaRecordApplicationProvider,
        caller_identity=caller_identity,
        media_record_repository=media_record_infrastructure.media_record_repository,
        transaction_manager=media_record_infrastructure.transaction_manager,
    )
