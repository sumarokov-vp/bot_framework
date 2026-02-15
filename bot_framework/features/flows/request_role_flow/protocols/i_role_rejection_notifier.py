from typing import Protocol

from bot_framework.core.entities.user import User


class IRoleRejectionNotifier(Protocol):
    def notify(self, user: User) -> None: ...
