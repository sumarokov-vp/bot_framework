from datetime import datetime
from typing import Protocol


class IRemainingTimeFormatter(Protocol):
    def format(self, expires_at: datetime, language_code: str) -> str: ...
