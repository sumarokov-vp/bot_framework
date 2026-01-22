from typing import Protocol

from bot_framework.base_protocols import (
    CreateProtocol,
    DeleteProtocol,
    GetByNameProtocol,
    ReadProtocol,
    UpdateProtocol,
)
from bot_framework.entities.user import User


class IUserRepo(
    GetByNameProtocol,
    CreateProtocol,
    DeleteProtocol,
    ReadProtocol,
    UpdateProtocol,
    Protocol,
):
    def get_by_role_name(
        self,
        role_name: str,
    ) -> list[User]: ...
