from typing import (
    Protocol,
    runtime_checkable,
)

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer


@runtime_checkable
class ICallbackHandler(Protocol):
    callback_answerer: ICallbackAnswerer
    prefix: str
    allowed_roles: set[str] | None

    def handle(self, callback: BotCallback) -> None: ...
