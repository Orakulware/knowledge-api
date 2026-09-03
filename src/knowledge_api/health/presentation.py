from collections.abc import Sequence
from typing import Annotated

from dependencies import get_db_session
from fastapi import APIRouter, Depends, Request, Response
from health.checks import (
    BrokerHealthCheck,
    ComponentStatus,
    DatabaseHealthCheck,
    HealthCheck,
    ResultBackendHealthCheck,
    check_all,
)
from media_record.infrastructure.consumer.consumer import MediaRecordConsumer
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

health_router = APIRouter(prefix="/health", tags=["Health"])


class LivenessResponseBody(BaseModel):
    status: ComponentStatus = Field(
        default=ComponentStatus.UP,
        examples=[ComponentStatus.UP],
    )


class ComponentHealthBody(BaseModel):
    name: str = Field(examples=["database"])
    status: ComponentStatus
    error: str | None = Field(default=None, examples=["ConnectionRefusedError"])


class ReadinessResponseBody(BaseModel):
    status: ComponentStatus
    components: list[ComponentHealthBody]


def get_media_record_consumer(request: Request) -> MediaRecordConsumer:
    consumer: MediaRecordConsumer = request.app.state.media_record_consumer
    return consumer


def get_health_checks(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    consumer: Annotated[MediaRecordConsumer, Depends(get_media_record_consumer)],
) -> Sequence[HealthCheck]:
    return (
        DatabaseHealthCheck(session=session),
        BrokerHealthCheck(consumer=consumer),
        ResultBackendHealthCheck(consumer=consumer),
    )


@health_router.get(
    path="/live/",
    summary="Liveness probe",
    description="Answers as long as the process can serve requests. "
    "Never touches a downstream component, so a failing dependency "
    "does not get the container restarted.",
)
async def liveness() -> LivenessResponseBody:
    return LivenessResponseBody()


@health_router.get(
    path="/ready/",
    summary="Readiness probe",
    description="Probes every downstream component the API needs to do work. "
    "Returns 503 while any of them is unreachable.",
    responses={503: {"model": ReadinessResponseBody}},
)
async def readiness(
    response: Response,
    checks: Annotated[Sequence[HealthCheck], Depends(get_health_checks)],
) -> ReadinessResponseBody:
    components = await check_all(checks)
    ready = all(component.status is ComponentStatus.UP for component in components)
    if not ready:
        response.status_code = 503
    return ReadinessResponseBody(
        status=ComponentStatus.UP if ready else ComponentStatus.DOWN,
        components=[
            ComponentHealthBody(
                name=component.name,
                status=component.status,
                error=component.error,
            )
            for component in components
        ],
    )
