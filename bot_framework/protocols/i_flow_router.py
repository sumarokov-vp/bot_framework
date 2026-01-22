from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from bot_framework.entities.user import User


@runtime_checkable
class IFlowRouter(Protocol):
    def get_name(self) -> str: ...

    def start(
        self,
        user: User,
        return_to: IFlowRouter | None = None,
    ) -> None: ...
