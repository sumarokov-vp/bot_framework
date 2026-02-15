from typing import Protocol

from bot_framework.core.entities.user import User


class IRoleListPresenter(Protocol):
    def present(self, user: User) -> None: ...
