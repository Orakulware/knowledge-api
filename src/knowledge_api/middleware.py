from datetime import timedelta
from typing import Any

from authx import AuthX, AuthXConfig, RateLimiter
from config import get_jwt_secret_key

TOKEN_TTL = timedelta(days=1)

AUTHX_CONFIG = AuthXConfig(
    JWT_SECRET_KEY=get_jwt_secret_key(),
    JWT_TOKEN_LOCATION=["headers", "cookies"],
    JWT_ACCESS_TOKEN_EXPIRES=TOKEN_TTL,
    JWT_COOKIE_SAMESITE="strict",
)

auth: AuthX[Any] = AuthX(config=AUTHX_CONFIG)
rate_limiter = RateLimiter(max_requests=10, window=10)
