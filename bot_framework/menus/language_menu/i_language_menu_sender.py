from typing import Protocol

from bot_framework.entities.user import User


class ILanguageMenuSender(Protocol):
    def send(self, user: User) -> None: ...
