from media_record.domain import MediaRecord
from media_record.infrastructure.mappings import registry
from sqlalchemy import (
    JSON,
    UUID,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
)

media_record_table = Table(
    "media_records",
    registry.mapping_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("added_by", UUID, nullable=False),
    Column(
        "posted_in_media",
        UUID,
        ForeignKey("media.id"),
        nullable=False,
        index=True,
    ),
    Column("content", String, nullable=False),
    Column("posted_at", DateTime(timezone=True), nullable=False),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
    Column("metadata", JSON, nullable=False, default=dict),
)


def map_media_record_table() -> None:
    registry.mapping_registry.map_imperatively(
        MediaRecord,
        media_record_table,
        properties={
            "added_by": media_record_table.c.added_by,
            "posted_in_media": media_record_table.c.posted_in_media,
            "content": media_record_table.c.content,
            "posted_at": media_record_table.c.posted_at,
            "deleted_at": media_record_table.c.deleted_at,
            "metadata": media_record_table.c.metadata,
        },
    )
