from typing import Protocol, TypeVar

from bot_framework.core.base_protocols import (
    CreateProtocol,
    DeleteProtocol,
    GetByNameProtocol,
    ReadProtocol,
    UpdateProtocol,
)
from bot_framework.core.entities.user import User

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

    def update_language(
        self,
        user_id: int,
        language_code: str,
    ) -> None: ...

    def set_phone_number(
        self,
        user_id: int,
        phone_number: str,
    ) -> None: ...
