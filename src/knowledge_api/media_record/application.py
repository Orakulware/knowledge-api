import logging
from dataclasses import dataclass

from media_record import domain
from shared.transaction_manager import TransactionManager

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PostMediaRecordRequest:
    submitter_id: str
    record: domain.MediaRecord


class PostMediaRecord:
    def __init__(self, transaction_manager: TransactionManager) -> None:
        pass

    async def __call__(self, request: PostMediaRecordRequest) -> None:
        raise NotImplementedError
