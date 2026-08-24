import datetime
import uuid
from typing import Annotated, Any

import middleware
from fastapi import APIRouter, Depends, Request
from media_record.domain import MediaType
from media_record.infrastructure.consumer.tasks import (
    PostMediaPayload,
    PostMediaRecordPayload,
)
from pydantic import BaseModel, Field
from schemas import ErrorResponse
from taskiq import AsyncTaskiqDecoratedTask

media_record_router = APIRouter(prefix="/api/v1/media-record", tags=["V1 Media Record"])


class PostMediaRecordRequestBody(BaseModel):
    posted_in_media: uuid.UUID
    content: str = Field(examples=["Breaking news content..."])
    posted_at: datetime.datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


def get_post_media_record_task(request: Request) -> AsyncTaskiqDecoratedTask:
    return request.app.state.post_media_record_task


@media_record_router.post(
    path="/media-record/",
    status_code=202,
    summary="Queue a media record for ingestion",
    dependencies=[
        Depends(middleware.rate_limiter),
        Depends(middleware.auth.access_token_required),
    ],
    responses={401: {"model": ErrorResponse}},
)
async def post_media_record(
    body: PostMediaRecordRequestBody,
    post_media_record_task: Annotated[
        AsyncTaskiqDecoratedTask,
        Depends(get_post_media_record_task),
    ],
) -> None:
    payload = PostMediaRecordPayload(
        posted_in_media=body.posted_in_media,
        content=body.content,
        posted_at=body.posted_at,
        metadata=body.metadata,
    )
    await post_media_record_task.kiq(payload=payload)


class PostMediaRequestBody(BaseModel):
    media_type: MediaType
    media_name: str = Field(examples=["The Daily Times"])
    metadata: dict[str, Any] = Field(default_factory=dict)


def get_post_media_task(request: Request) -> AsyncTaskiqDecoratedTask:
    return request.app.state.post_media_task


@media_record_router.post(
    path="/media/",
    status_code=202,
    summary="Register a new media source",
    dependencies=[
        Depends(middleware.rate_limiter),
        Depends(middleware.auth.access_token_required),
    ],
    responses={401: {"model": ErrorResponse}},
)
async def post_media(
    body: PostMediaRequestBody,
    post_media_task: Annotated[AsyncTaskiqDecoratedTask, Depends(get_post_media_task)],
) -> None:
    payload = PostMediaPayload(
        media_type=body.media_type,
        media_name=body.media_name,
        metadata=body.metadata,
    )
    await post_media_task.kiq(payload=payload)
