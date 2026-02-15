from typing import (
    Protocol,
    runtime_checkable,
)

from bot_framework.core.entities.bot_message import BotMessage


@runtime_checkable
class IMessageHandler(Protocol):
    allowed_roles: set[str] | None

    def handle(
        self,
        message: BotMessage,
    ) -> bool | None: ...
