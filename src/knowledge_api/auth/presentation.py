from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

auth_router = APIRouter()

class LoginRequestBody(BaseModel):
    username: str
    password: str


class LoginResponseBody(BaseModel):
    access_token: str


@app.post("/login/", dependencies=Depends(rate_limiter))
async def login(lrb: LoginRequestBody) -> LoginResponseBody | HTTPException:
    if lrb.username == "admin" and lrb.password == "admin":
        token = auth.create_access_token(uid=lrb.username)
        return LoginResponseBody(access_token=token)
    return HTTPException(status_code=403, detail="Credentials didn't match")
