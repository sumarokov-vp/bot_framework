from __future__ import annotations

from typing import Protocol

from bot_framework.core.protocols.i_callback_handler import ICallbackHandler


class ICallbackHandlerRegistry(Protocol):
    def register(self, handler: ICallbackHandler) -> None: ...
