from typing import Protocol

from bot_framework.entities.role import Role
from bot_framework.entities.user import User


class IRoleRequestSender(Protocol):
    def send_to_supervisors(
        self,
        requester: User,
        role: Role,
    ) -> None: ...
