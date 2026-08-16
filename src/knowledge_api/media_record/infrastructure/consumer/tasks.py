import dataclasses
import datetime
import logging
import uuid
from typing import Any

from dependency_injector.wiring import Provide, inject
from media_record.application import PostMediaRecord, PostMediaRecordRequest
from setup.containers import Container

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class PostMediaRecordPayload:
    posted_in_media: uuid.UUID
    content: str
    posted_at: datetime.datetime
    metadata: dict[str, Any]


@inject
async def post_media_record(
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
    await interactor(request=request)
