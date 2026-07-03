from typing import Annotated

import middleware
from config import AuthCredsConfig
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field
from schemas import AppError, ErrorResponse

TOKEN_TTL = 60 * 60 * 24  # 1 day
auth_router = APIRouter()


class LoginRequestBody(BaseModel):
    username: str = Field(examples=["jonh_doe13"])
    password: str = Field(examples=["your_strong_password"])


class LoginResponseBody(BaseModel):
    access_token: str = Field(examples=["access_token"])


class LogoutResponseBody(BaseModel):
    message: str = Field(default="successful logout", examples=["successful logout"])


@auth_router.post(
    "/login/",
    dependencies=[Depends(middleware.rate_limiter)],
    responses={403: {"model": ErrorResponse}},
)
async def login(
    response: Response,
    lrb: LoginRequestBody,
    creds: Annotated[AuthCredsConfig, Depends(AuthCredsConfig)],
) -> LoginResponseBody:
    if lrb.username == creds.access_username and lrb.password == creds.access_password:
        token = middleware.auth.create_access_token(uid=lrb.username)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=TOKEN_TTL,
        )
        return LoginResponseBody(access_token=token)
    raise AppError(
        status_code=403,
        code="INVALID_CREDENTIALS",
        detail="Credentials didn't match",
    )


@auth_router.delete(
    path="/logout/",
    dependencies=[
        Depends(middleware.rate_limiter),
        Depends(middleware.auth.access_token_required),
    ],
    responses={401: {"model": ErrorResponse}},
)
async def logout(response: Response) -> LogoutResponseBody:
    response.delete_cookie(key="access_token")
    return LogoutResponseBody()
