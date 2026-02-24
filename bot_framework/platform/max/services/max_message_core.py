from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard

if TYPE_CHECKING:
    from bot_framework.domain.flow_management.protocols.i_flow_message_storage import (
        IFlowMessageStorage,
    )
    from bot_framework.platform.max.middleware.ensure_user_middleware import (
        MaxEnsureUserMiddleware,
    )

from .max_api_client import MaxApiClient
from .max_callback_answerer import MaxCallbackAnswerer
from .max_callback_handler_registry import MaxCallbackHandlerRegistry
from .max_message_handler_registry import MaxMessageHandlerRegistry
from .max_messenger import MaxMessenger
from .max_polling import MaxPolling


class MaxMessageCore:
    def __init__(
        self,
        token: str,
        flow_message_storage: IFlowMessageStorage | None = None,
        ensure_user_middleware: MaxEnsureUserMiddleware | None = None,
    ) -> None:
        self.flow_message_storage = flow_message_storage
        self.ensure_user_middleware = ensure_user_middleware
        self._mid_to_int: dict[str, int] = {}
        self._int_to_mid: dict[int, str] = {}
        self.api_client = MaxApiClient(token)
        self._init_components()

    def _init_components(self) -> None:
        messenger = MaxMessenger(self)
        self.message_sender: MaxMessenger = messenger
        self.message_replacer: MaxMessenger = messenger
        self.message_deleter: MaxMessenger = messenger
        self.document_sender: MaxMessenger = messenger
        self.document_downloader: MaxMessenger = messenger

        self.callback_answerer: MaxCallbackAnswerer = MaxCallbackAnswerer(self)
        self.callback_handler_registry: MaxCallbackHandlerRegistry = MaxCallbackHandlerRegistry()
        self.message_handler_registry: MaxMessageHandlerRegistry = MaxMessageHandlerRegistry()
        self._polling: MaxPolling = MaxPolling(self)

    @property
    def mid_to_int(self) -> dict[str, int]:
        return self._mid_to_int

    def register_mid(self, mid: str) -> int:
        if mid in self._mid_to_int:
            return self._mid_to_int[mid]
        int_id = hash(mid) & 0x7FFFFFFF
        while int_id in self._int_to_mid and self._int_to_mid[int_id] != mid:
            int_id = (int_id + 1) & 0x7FFFFFFF
        self._mid_to_int[mid] = int_id
        self._int_to_mid[int_id] = mid
        return int_id

    def int_to_mid(self, int_id: int) -> str:
        return self._int_to_mid.get(int_id, str(int_id))

    def convert_keyboard(self, keyboard: Keyboard) -> dict[str, Any]:
        buttons = [
            [
                {
                    "type": "callback",
                    "text": button.text,
                    "payload": button.callback_data,
                }
                for button in row
            ]
            for row in keyboard.rows
        ]
        return {
            "type": "inline_keyboard",
            "payload": {"buttons": buttons},
        }

    def create_bot_message(self, chat_id: int, message_data: dict[str, Any]) -> BotMessage:
        body = message_data.get("body", {})
        raw_mid = body.get("mid", "")
        message_id = self.register_mid(raw_mid) if raw_mid else 0

        sender = message_data.get("sender", {})
        user_id = int(sender.get("user_id", 0)) if sender else None

        text = body.get("text")
        return BotMessage(
            chat_id=chat_id,
            message_id=message_id,
            user_id=user_id,
            text=text,
        )

    def register_message(
        self,
        chat_id: int,
        message_id: int,
        flow_name: str | None,
    ) -> None:
        if flow_name and self.flow_message_storage:
            self.flow_message_storage.add_message(
                telegram_id=chat_id,
                flow_name=flow_name,
                message_id=message_id,
            )

    def run(self) -> None:
        self._polling.run()
