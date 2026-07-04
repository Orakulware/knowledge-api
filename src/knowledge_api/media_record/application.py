import datetime
import logging
import uuid
from dataclasses import dataclass
from typing import Any

from media_record import domain
from media_record.infrastructure.exception import MediaRecordRepositoryError
from media_record.infrastructure.infrastructure import MediaRecordRepository
from shared.caller_identity import CallerIdentity
from shared.transaction_manager import TransactionManager

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PostMediaRecordRequest:
    posted_in_media: uuid.UUID
    content: str
    posted_at: datetime.datetime
    metadata: dict[str, Any]


class PostMediaRecord:
    def __init__(
        self,
        caller_identity: CallerIdentity,
        transaction_manager: TransactionManager,
        media_record_repository: MediaRecordRepository,
    ) -> None:
        self._caller_identity = caller_identity
        self._transaction_manager = transaction_manager
        self._media_record_repository = media_record_repository

    async def __call__(self, request: PostMediaRecordRequest) -> None:
        media_record = domain.MediaRecord(
            added_by=self._caller_identity.id,
            content=request.content,
            deleted_at=None,
            metadata=request.metadata,
            posted_at=request.posted_at,
            posted_in_media=request.posted_in_media,
        )
        try:
            await self._media_record_repository.save_media_record(
                media_record=media_record,
            )
        except MediaRecordRepositoryError:
            logger.exception(msg="Failed to save media record")
            await self._transaction_manager.rollback()
            return

        await self._transaction_manager.commit()
