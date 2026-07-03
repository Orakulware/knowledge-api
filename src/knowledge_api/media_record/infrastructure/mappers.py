from media_record.infrastructure.mappings.media import map_media_table
from media_record.infrastructure.mappings.media_record import map_media_record_table


def map_all() -> None:
    map_media_table()
    map_media_record_table()
