from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import middleware
import setup
from auth import presentation as auth_presentation
from config import PostgresConfig
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from media_record import presentation as media_record_presentation
from media_record.infrastructure import consumer
from schemas import AppError, ErrorResponse
from shared.database import SQLAlchemyDatabase

__all__ = ["AppError", "ErrorResponse"]


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    await consumer.broker.startup()
    yield
    await consumer.broker.shutdown()


app = FastAPI(lifespan=lifespan)
app.state.container = setup.bootstrap()
app.state.database = SQLAlchemyDatabase(config=PostgresConfig.from_env())
app.include_router(auth_presentation.auth_router)
app.include_router(media_record_presentation.media_record_router)
middleware.auth.handle_errors(app=app)


@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "detail": exc.detail},
    )
