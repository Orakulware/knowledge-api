from abc import ABC, abstractmethod

from media_record.domain import MediaRecord
from media_record.infrastructure.error_mapper import map_integrity_error
from media_record.infrastructure.mappings.media_record import media_record_table
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class MediaRecordRepository(ABC):
    @abstractmethod
    async def save_media_record(self, media_record: MediaRecord) -> None: ...


class SQLAlchemyRecordRepository(MediaRecordRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def save_media_record(self, media_record: MediaRecord) -> None:
        stmt = insert(media_record_table).values(
            id=media_record.id,
            added_by=media_record.added_by,
            posted_in_media=media_record.posted_in_media,
            content=media_record.content,
            posted_at=media_record.posted_at,
            deleted_at=media_record.deleted_at,
            metadata=media_record.metadata,
        )
        try:
            await self._session.execute(stmt)
        except IntegrityError as error:
            raise map_integrity_error(error) from error
