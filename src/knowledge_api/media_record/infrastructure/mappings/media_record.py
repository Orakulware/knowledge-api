from media_record.domain import MediaRecord
from media_record.infrastructure.mappings import registry
from sqlalchemy import (
    JSON,
    UUID,
    Column,
    DateTime,
    String,
    Table,
)

media_record_table = Table(
    "media_records",
    registry.mapping_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("posted_by", String, nullable=False),
    Column("content", String, nullable=False),
    Column("posted_at", DateTime, nullable=False),
    Column("deleted_at", DateTime, nullable=True),
    Column("metadata", JSON, nullable=False, default=dict),
)


def map_media_record_table() -> None:
    registry.mapping_registry.map_imperatively(
        MediaRecord,
        media_record_table,
        properties={
            "posted_by": media_record_table.c.posted_by,
            "content": media_record_table.c.content,
            "posted_at": media_record_table.c.posted_at,
            "deleted_at": media_record_table.c.deleted_at,
            "metadata": media_record_table.c.metadata,
        },
    )
