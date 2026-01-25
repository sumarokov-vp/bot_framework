from typing import Protocol

from bot_framework.entities.user import User


class IMainMenuSender(Protocol):
    def send(self, user: User) -> None: ...
