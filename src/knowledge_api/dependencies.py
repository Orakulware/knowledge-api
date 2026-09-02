import uuid
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from shared.caller_identity import CallerIdentity, IdentityRole
from shared.database import SQLAlchemyDatabase
from shared.transaction_manager import (
    SQLAlchemySessionTransactionManager,
    TransactionManager,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession]:
    database: SQLAlchemyDatabase = request.app.state.database
    async with database.get_session() as session:
        yield session


def get_transaction_manager(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TransactionManager:
    return SQLAlchemySessionTransactionManager(session=session)


def get_caller_identity() -> CallerIdentity:
    # TODO: derive the real caller id/role once user accounts exist.
    # access_token_required today only guarantees a valid JWT with
    # `sub=username` - there is no uuid/role to decode yet.
    return CallerIdentity(id=uuid.UUID(int=0), role=IdentityRole.ADMIN)
