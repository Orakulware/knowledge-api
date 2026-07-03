import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any


class MediaType(StrEnum):
    TELEGRAM = "TELEGRAM"
    NEWSPAPER = "NEWSPAPER"


class Media:
    """Model of media table.
    Contains id key, media type and media name and reputation"""

    id: uuid.UUID
    media_type: MediaType
    media_name: str
    reputation: float


class MediaRecord:
    """Model of media_records table.
    Contains the media records, including it's content,
    a timestamp and contributor acknowledgements.
    """

    id: uuid.UUID
    added_by: str
    posted_in_media: uuid.UUID
    content: str
    posted_at: datetime
    deleted_at: datetime | None
    metadata: dict[str, Any]

    def __init__(  # noqa: PLR0913
        self,
        added_by: str,
        posted_in_media: uuid.UUID,
        content: str,
        posted_at: datetime,
        deleted_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if metadata is None:
            metadata = {}
        # UUIDv7 best for creating an index.
        self.id = uuid.uuid7()
        self.added_by = added_by
        self.posted_in_media = posted_in_media
        self.content = content
        self.posted_at = posted_at
        self.deleted_at = deleted_at
        self.metadata = metadata

    def __str__(self) -> str:
        return f"{self.added_by}[{self.posted_at}]: \
            {self.content} \n Metadata: {self.metadata}"
