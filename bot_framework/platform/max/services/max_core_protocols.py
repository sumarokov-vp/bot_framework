from __future__ import annotations

from typing import Any, Protocol

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.platform.max.middleware.ensure_user_middleware import MaxEnsureUserMiddleware
from bot_framework.platform.max.repos import MaxDialogRepo

from .max_api_client import MaxApiClient
from .max_callback_handler_registry import MaxCallbackHandlerRegistry
from .max_message_handler_registry import MaxMessageHandlerRegistry
from .max_next_step_handler_registrar import MaxNextStepHandlerRegistrar


class IMaxCallbackCore(Protocol):
    api_client: MaxApiClient


class IMaxMessengerCore(Protocol):
    api_client: MaxApiClient
    dialog_repo: MaxDialogRepo

    def create_bot_message(self, chat_id: int, msg: dict[str, Any]) -> BotMessage: ...

    def register_message(self, chat_id: int, message_id: int, flow_name: str | None) -> None: ...

    def int_to_mid(self, int_id: int) -> str: ...

    def convert_keyboard(self, keyboard: Keyboard) -> dict[str, Any]: ...


class IMaxPollingCore(Protocol):
    api_client: MaxApiClient
    dialog_repo: MaxDialogRepo
    ensure_user_middleware: MaxEnsureUserMiddleware | None
    message_handler_registry: MaxMessageHandlerRegistry
    callback_handler_registry: MaxCallbackHandlerRegistry

    @property
    def next_step_registrar(self) -> MaxNextStepHandlerRegistrar: ...
    @property
    def mid_to_int(self) -> dict[str, int]: ...

    def register_mid(self, mid: str) -> int: ...
