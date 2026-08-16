from dependency_injector.wiring import Provide, inject
from media_record.application import PostMediaRecord
from setup.containers import Container


@inject
async def post_media_record(
    interactor: PostMediaRecord = Provide[
        Container.media_record_application.post_media_record
    ],
) -> None: ...
