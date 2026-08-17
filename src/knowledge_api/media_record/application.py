import datetime
import logging
import uuid
from dataclasses import dataclass
from typing import Any

from media_record import domain
from media_record.exception import (
    DuplicateMediaError,
    DuplicateMediaRecordError,
    InvalidMediaReferenceError,
    MediaRecordSaveError,
    MediaSaveError,
)
from media_record.infrastructure import exception as infrastructure_exception
from media_record.infrastructure.infrastructure import (
    MediaRecordRepository,
    MediaRepository,
)
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
        except infrastructure_exception.DuplicateMediaRecordError as error:
            logger.exception(msg="Media record with this id already exists")
            await self._transaction_manager.rollback()
            raise DuplicateMediaRecordError from error
        except infrastructure_exception.InvalidMediaReferenceError as error:
            logger.exception(msg="Media record references a non-existent media")
            await self._transaction_manager.rollback()
            raise InvalidMediaReferenceError from error
        except infrastructure_exception.MediaRecordConstraintViolationError as error:
            logger.exception(
                msg="Failed to save media record due to a constraint violation",
            )
            await self._transaction_manager.rollback()
            raise MediaRecordSaveError from error

        await self._transaction_manager.commit()


@dataclass(frozen=True, slots=True)
class PostMediaRequest:
    media_type: domain.MediaType
    media_name: str


class PostMedia:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        media_repository: MediaRepository,
    ) -> None:
        self._transaction_manager = transaction_manager
        self._media_repository = media_repository

    async def __call__(self, request: PostMediaRequest) -> None:
        media = domain.Media(
            media_type=request.media_type,
            media_name=request.media_name,
        )
        try:
            await self._media_repository.save_media(media=media)
        except infrastructure_exception.DuplicateMediaError as error:
            logger.exception(msg="Media with this type/name already exists")
            await self._transaction_manager.rollback()
            raise DuplicateMediaError from error
        except infrastructure_exception.MediaConstraintViolationError as error:
            logger.exception(msg="Failed to save media due to a constraint violation")
            await self._transaction_manager.rollback()
            raise MediaSaveError from error

        await self._transaction_manager.commit()
