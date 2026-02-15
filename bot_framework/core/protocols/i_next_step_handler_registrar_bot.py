from collections.abc import Callable
from typing import Any, Protocol


class INextStepHandlerRegistrarBot(Protocol):
    def register_next_step_handler(
        self,
        message: Any,
        callback: Callable[..., Any],
    ) -> None: ...
