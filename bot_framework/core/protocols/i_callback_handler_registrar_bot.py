from collections.abc import Callable
from typing import Any, Protocol


class ICallbackHandlerRegistrarBot(Protocol):
    def register_callback_query_handler(
        self,
        callback: Callable[..., Any],
        func: Callable[..., bool] | None = None,
    ) -> None: ...
