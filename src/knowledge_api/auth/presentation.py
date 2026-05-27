from typing import Any

from authx import AuthX, AuthXConfig, RateLimiter
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

auth_router = FastAPI()

AUTHX_CONFIG = AuthXConfig(
    JWT_SECRET_KEY="secret-hardcoded",
    JWT_TOKEN_LOCATION=["headers"],
)

auth: AuthX[Any] = AuthX(config=AUTHX_CONFIG)
auth.handle_errors(app=auth_router)
rate_limiter = RateLimiter(max_requests=10, window=10)

class LoginRequestBody(BaseModel):
    username: str
    password: str


class LoginResponseBody(BaseModel):
    access_token: str


@auth_router.post("/login/", dependencies=Depends(rate_limiter))
async def login(lrb: LoginRequestBody) -> LoginResponseBody | HTTPException:
    if lrb.username == "admin" and lrb.password == "admin":
        token = auth.create_access_token(uid=lrb.username)
        return LoginResponseBody(access_token=token)
    return HTTPException(status_code=403, detail="Credentials didn't match")
