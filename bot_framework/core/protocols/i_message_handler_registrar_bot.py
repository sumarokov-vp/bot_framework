from collections.abc import Callable
from typing import Any, Protocol


class IMessageHandlerRegistrarBot(Protocol):
    def register_message_handler(
        self,
        callback: Callable[..., Any],
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[..., bool] | None = None,
    ) -> None: ...
