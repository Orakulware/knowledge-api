from abc import ABC, abstractmethod

from media_record.domain import MediaRecord
from sqlalchemy.ext.asyncio import AsyncSession


class MediaRecordRepository(ABC):
    @abstractmethod
    async def save_media_record(self, media_record: MediaRecord) -> None: ...


class SQLAlchemyRecordRepository(MediaRecordRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def save_media_record(self, media_record: MediaRecord) -> None:
        pass
