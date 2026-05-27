from typing import Any

from authx import AuthX, AuthXConfig, RateLimiter

AUTHX_CONFIG = AuthXConfig(
    JWT_SECRET_KEY="secret-hardcoded",
    JWT_TOKEN_LOCATION=["headers"],
)

auth: AuthX[Any] = AuthX(config=AUTHX_CONFIG)
rate_limiter = RateLimiter(max_requests=10, window=10)
