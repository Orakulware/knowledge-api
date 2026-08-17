from media_record.domain import Media, MediaType
from media_record.infrastructure.mappings import registry
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    Float,
    String,
    Table,
    UniqueConstraint,
)

media_table = Table(
    "media",
    registry.mapping_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("media_type", Enum(MediaType, create_constraint=True), nullable=False),
    Column("media_name", String, nullable=False),
    Column("reputation", Float, nullable=False),
    Column("added_at", DateTime(timezone=True), nullable=False),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
    UniqueConstraint(
        "media_type",
        "media_name",
    ),  # uq_media_media_type according to registry.py
)


def map_media_table() -> None:
    registry.mapping_registry.map_imperatively(
        Media,
        media_table,
        properties={
            "media_type": media_table.c.media_type,
            "media_name": media_table.c.media_name,
            "reputation": media_table.c.reputation,
            "added_at": media_table.c.added_at,
            "deleted_at": media_table.c.deleted_at,
        },
    )
