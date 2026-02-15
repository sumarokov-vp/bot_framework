from typing import Protocol

from bot_framework.core.entities.user import User


class IRequestRoleFlowRouter(Protocol):
    def start(self, user: User) -> None: ...
