from fastapi import HTTPException
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(examples=["INVALID_CREDENTIALS", "TOKEN_EXPIRED"])
    detail: str = Field(examples=["Credentials didn't match", "Token has expired"])


class AppError(HTTPException):
    def __init__(self, status_code: int, code: str, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.code = code
