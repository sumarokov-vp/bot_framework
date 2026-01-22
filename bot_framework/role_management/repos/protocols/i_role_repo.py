from typing import Protocol

from bot_framework.base_protocols import (
    GetAllProtocol,
    ReadProtocol,
)
from bot_framework.entities.role import Role


class IRoleRepo(
    GetAllProtocol,
    ReadProtocol,
    Protocol,
):
    def get_user_roles(
        self,
        user_id: int,
    ) -> list[Role]: ...

    def assign_role(
        self,
        user_id: int,
        role_id: int,
    ) -> None: ...

    def assign_role_by_name(
        self,
        user_id: int,
        role_name: str,
    ) -> None: ...
