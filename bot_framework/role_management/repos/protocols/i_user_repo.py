from typing import Protocol, TypeVar

from bot_framework.base_protocols import (
    CreateProtocol,
    DeleteProtocol,
    GetByNameProtocol,
    ReadProtocol,
    UpdateProtocol,
)
from bot_framework.entities.user import User

UserT = TypeVar("UserT", bound=User)


class IUserRepo(
    GetByNameProtocol[UserT],
    CreateProtocol[UserT],
    DeleteProtocol[UserT],
    ReadProtocol[UserT],
    UpdateProtocol[UserT],
    Protocol[UserT],
):
    def get_by_role_name(
        self,
        role_name: str,
    ) -> list[UserT]: ...
