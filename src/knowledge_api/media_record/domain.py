from datetime import datetime
from typing import Any


class MediaRecord:
    def __init__(
        self,
        posted_in: str,
        content: str,
        posted_at: datetime,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if metadata is None:
            metadata = {}
        self._posted_in = posted_in
        self._content = content
        self._posted_at = posted_at
        self._metadata = metadata

    def __str__(self) -> str:
        return f"{self._posted_in}[{self._posted_at}]: \
            {self._content} \n Metadata: {self._metadata}"
