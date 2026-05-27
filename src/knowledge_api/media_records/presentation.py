from fastapi import APIRouter, Depends

from knowledge_api import middleware
from knowledge_api.schemas import AppError

media_record_router = APIRouter()

@media_record_router.post(
    path="/",
    dependencies=[
        Depends(middleware.rate_limiter),
        Depends(middleware.auth.access_token_required),
    ],
)
async def post_media_record() -> None:
    raise AppError(
        status_code=500,
        code="NOT_IMPLEMENTED",
        detail="Not implemented",
    )
