from functools import cache

import dependencies
from media_record.infrastructure.mappers import map_all
from setup.containers import Container


@cache
def bootstrap() -> Container:
    # Deferred: tasks.py imports setup.containers, which would re-trigger this
    # module's own import (and cycle) if imported at module level here.
    from media_record.infrastructure.consumer import (  # noqa: PLC0415
        tasks as media_record_tasks,
    )

    map_all()
    container = Container()
    container.wire(modules=[dependencies, media_record_tasks])
    return container
