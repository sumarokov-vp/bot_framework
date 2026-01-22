from typing import Protocol

from bot_framework.entities.bot_user import BotUser


class IEnsureUserExists(Protocol):
    def execute(self, user: BotUser) -> None: ...
