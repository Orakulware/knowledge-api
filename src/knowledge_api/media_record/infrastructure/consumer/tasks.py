import dataclasses
import datetime
import logging
import uuid
from typing import Any

from dependency_injector.wiring import Provide, inject
from media_record.application import PostMediaRecord, PostMediaRecordRequest
from media_record.exception import (
    DuplicateMediaRecordError,
    InvalidMediaReferenceError,
    MediaRecordSaveError,
)
from setup.containers import Container
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class PostMediaRecordPayload:
    posted_in_media: uuid.UUID
    content: str
    posted_at: datetime.datetime
    metadata: dict[str, Any]


@inject
async def _post_media_record(
    payload: PostMediaRecordPayload,
    interactor: PostMediaRecord = Provide[
        Container.media_record_application.post_media_record
    ],
) -> None:
    logger.info("Received the post media record payload")
    request = PostMediaRecordRequest(
        posted_in_media=payload.posted_in_media,
        content=payload.content,
        posted_at=payload.posted_at,
        metadata=payload.metadata,
    )
    try:
        await interactor(request=request)
    except (
        DuplicateMediaRecordError,
        InvalidMediaReferenceError,
        MediaRecordSaveError,
    ):
        logger.exception("Failed to post media record")
        raise


def register_tasks(broker: AsyncBroker) -> AsyncTaskiqDecoratedTask:
    return broker.register_task(_post_media_record, task_name="post_media_record")
