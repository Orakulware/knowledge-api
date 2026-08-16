from collections.abc import AsyncGenerator

from dependency_injector import containers, providers
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
