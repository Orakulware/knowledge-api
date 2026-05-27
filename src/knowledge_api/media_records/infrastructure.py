from abc import ABC, abstractmethod


class MediaRecordRepository(ABC):
    @abstractmethod
    async def save_media_record(self) -> None:
        ...

class SQLAlchemyRecordRepository(MediaRecordRepository):
    def __init__(self) -> None:
        super().__init__()

    async def save_media_record(self) -> None:
        raise NotImplementedError
