import datetime
import uuid
from typing import Annotated, Any

import middleware
from dependencies import get_caller_identity, get_db_session
from fastapi import APIRouter, Depends
from media_record.application import PostMediaRecord, PostMediaRecordRequest
from media_record.exception import (
    DuplicateMediaRecordError,
    InvalidMediaReferenceError,
    MediaRecordSaveError,
)
from media_record.infrastructure.infrastructure import (
    MediaRecordRepository,
    SQLAlchemyRecordRepository,
)
from pydantic import BaseModel, Field
from schemas import AppError, ErrorResponse
from shared.caller_identity import CallerIdentity
from shared.transaction_manager import (
    SQLAlchemySessionTransactionManager,
    TransactionManager,
)
from sqlalchemy.ext.asyncio import AsyncSession

media_record_router = APIRouter()


class PostMediaRecordRequestBody(BaseModel):
    posted_in_media: uuid.UUID
    content: str = Field(examples=["Breaking news content..."])
    posted_at: datetime.datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


def get_media_record_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> MediaRecordRepository:
    return SQLAlchemyRecordRepository(session=session)


def get_transaction_manager(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TransactionManager:
    return SQLAlchemySessionTransactionManager(session=session)


def get_post_media_record(
    caller_identity: Annotated[CallerIdentity, Depends(get_caller_identity)],
    transaction_manager: Annotated[
        TransactionManager,
        Depends(get_transaction_manager),
    ],
    media_record_repository: Annotated[
        MediaRecordRepository,
        Depends(get_media_record_repository),
    ],
) -> PostMediaRecord:
    return PostMediaRecord(
        caller_identity=caller_identity,
        transaction_manager=transaction_manager,
        media_record_repository=media_record_repository,
    )


@media_record_router.post(
    path="/",
    dependencies=[
        Depends(middleware.rate_limiter),
        Depends(middleware.auth.access_token_required),
    ],
    responses={
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def post_media_record(
    body: PostMediaRecordRequestBody,
    post_media_record: Annotated[PostMediaRecord, Depends(get_post_media_record)],
) -> None:
    request = PostMediaRecordRequest(
        posted_in_media=body.posted_in_media,
        content=body.content,
        posted_at=body.posted_at,
        metadata=body.metadata,
    )
    try:
        await post_media_record(request=request)
    except DuplicateMediaRecordError as error:
        raise AppError(
            status_code=409,
            code="MEDIA_RECORD_ALREADY_EXISTS",
            detail="A media record with this id already exists",
        ) from error
    except InvalidMediaReferenceError as error:
        raise AppError(
            status_code=422,
            code="INVALID_MEDIA_REFERENCE",
            detail="The referenced media does not exist",
        ) from error
    except MediaRecordSaveError as error:
        raise AppError(
            status_code=500,
            code="MEDIA_RECORD_SAVE_FAILED",
            detail="Failed to save media record",
        ) from error
