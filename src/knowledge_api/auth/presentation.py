from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from knowledge_api import middleware
from knowledge_api.schemas import AppError, ErrorResponse

auth_router = APIRouter()


class LoginRequestBody(BaseModel):
    username: str = Field(examples=["jonh_doe13"])
    password: str = Field(examples=["your_strong_password"])


class LoginResponseBody(BaseModel):
    access_token: str = Field(examples=["access_token"])


@auth_router.post(
    "/login/",
    dependencies=[Depends(middleware.rate_limiter)],
    responses={403: {"model": ErrorResponse}},
)
async def login(lrb: LoginRequestBody) -> LoginResponseBody:
    if lrb.username == "admin" and lrb.password == "admin":
        token = middleware.auth.create_access_token(uid=lrb.username)
        return LoginResponseBody(access_token=token)
    raise AppError(
        status_code=403,
        code="INVALID_CREDENTIALS",
        detail="Credentials didn't match",
    )
