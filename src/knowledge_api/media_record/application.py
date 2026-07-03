import logging
from dataclasses import dataclass

from media_record import domain
from media_record.infrastructure.infrastructure import MediaRecordRepository
from shared.caller_identity import CallerIdentity
from shared.transaction_manager import TransactionManager

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PostMediaRecordRequest:
    record: domain.MediaRecord


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
        raise NotImplementedError
