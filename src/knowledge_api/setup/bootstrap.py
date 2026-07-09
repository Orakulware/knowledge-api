import dependencies
from media_record import presentation as media_record_presentation
from media_record.infrastructure.mappers import map_all
from setup.containers import Container


def bootstrap() -> Container:
    map_all()
    container = Container()
    container.wire(modules=[dependencies, media_record_presentation])
    return container
