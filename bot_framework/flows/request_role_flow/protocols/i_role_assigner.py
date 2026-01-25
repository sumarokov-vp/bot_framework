from typing import Protocol

from bot_framework.entities.user import User


class IRoleAssigner(Protocol):
    def assign_and_notify(
        self,
        user: User,
        role_id: int,
    ) -> None: ...
