import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

import middleware
import setup
from auth import presentation as auth_presentation
from config import PostgresConfig
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from health import presentation as health_presentation
from media_record import presentation as media_record_presentation
from media_record.infrastructure.consumer import tasks as media_record_tasks
from schemas import AppError, ErrorResponse
from shared.database import SQLAlchemyDatabase
from taskiq.api import run_receiver_task

__all__ = ["AppError", "ErrorResponse"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    container = app.state.container
    consumer = container.media_record_infrastructure.media_record_consumer()
    broker = consumer.broker
    app.state.media_record_consumer = consumer

    app.state.post_media_record_task, app.state.post_media_task = (
        media_record_tasks.register_tasks(broker)
    )

    # AioPikaBroker only opens its read channel (needed to consume messages)
    # when is_worker_process is True - normally set by the `taskiq worker` CLI.
    # We run the receiver in this same process instead, so set it ourselves
    # before startup opens both the write and read channels in one pass.
    broker.is_worker_process = True
    await consumer.startup()
    receiver_task = asyncio.create_task(run_receiver_task(broker))
    yield
    receiver_task.cancel()
    with suppress(asyncio.CancelledError):
        await receiver_task
    await consumer.shutdown()


tags_metadata = [
    {
        "name": "V1 Media Record",
        "description": "V1 Ingest media sources and the records posted to them.",
    },
    {
        "name": "Health",
        "description": "Liveness and readiness probes for orchestrators.",
    },
]

app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)
app.state.container = setup.bootstrap()
app.state.database = SQLAlchemyDatabase(config=PostgresConfig.from_env())
app.include_router(auth_presentation.auth_router)
app.include_router(media_record_presentation.media_record_router)
app.include_router(health_presentation.health_router)
middleware.auth.handle_errors(app=app)


@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "detail": exc.detail},
    )
