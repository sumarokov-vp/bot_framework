from datetime import UTC, datetime

from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import (
    IPhraseRepo,
)
from bot_framework.core.protocols import IRemainingTimeFormatter


class RemainingTimeFormatter(IRemainingTimeFormatter):
    def __init__(self, phrase_repo: IPhraseRepo) -> None:
        self._phrase_repo = phrase_repo

    def format(self, expires_at: datetime, language_code: str) -> str:
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)

        remaining = expires_at - datetime.now(UTC)
        total_minutes = max(0, int(remaining.total_seconds() // 60))
        hours = total_minutes // 60
        minutes = total_minutes % 60

        hours_suffix = self._phrase_repo.get_phrase(
            key="shared.time.hours_short",
            language_code=language_code,
        )
        minutes_suffix = self._phrase_repo.get_phrase(
            key="shared.time.minutes_short",
            language_code=language_code,
        )

        if hours > 0:
            return f"{hours}{hours_suffix} {minutes}{minutes_suffix}"
        return f"{minutes}{minutes_suffix}"
