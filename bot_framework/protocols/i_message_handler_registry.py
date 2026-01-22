from collections.abc import Callable
from typing import Protocol

from bot_framework.protocols.i_message_handler import IMessageHandler


class IMessageHandlerRegistry(Protocol):
    def register(
        self,
        handler: IMessageHandler,
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[..., bool] | None = None,
    ) -> None: ...
