from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from knowledge_api import middleware
from knowledge_api.auth import presentation
from knowledge_api.schemas import AppError, ErrorResponse

__all__ = ["AppError", "ErrorResponse"]

app = FastAPI()
app.include_router(presentation.auth_router)
middleware.auth.handle_errors(app=app)


@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "detail": exc.detail},
    )
