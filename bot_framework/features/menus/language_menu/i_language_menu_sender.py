from typing import Protocol

from bot_framework.core.entities.user import User


class ILanguageMenuSender(Protocol):
    def send(self, user: User) -> None: ...

    def replace(self, user: User, message_id: int) -> None: ...
