from collections.abc import AsyncGenerator

from config import PostgresConfig
from dependency_injector import containers, providers
from shared.database import SQLAlchemyDatabase
from sqlalchemy.ext.asyncio import AsyncSession


async def _db_session(database: SQLAlchemyDatabase) -> AsyncGenerator[AsyncSession]:
    async with database.get_session() as session:
        yield session


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(PostgresConfig.from_env)
    database = providers.Singleton(SQLAlchemyDatabase, config=config)
    db_session = providers.ContextLocalResource(_db_session, database=database)
