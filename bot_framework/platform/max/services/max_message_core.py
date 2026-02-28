from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.platform.max.repos import MaxDialogRepo

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
from .max_mid_registry import MaxMidRegistry
from .max_next_step_handler_registrar import MaxNextStepHandlerRegistrar
from .max_polling import MaxPolling


class MaxMessageCore:
    def __init__(
        self,
        api_client: MaxApiClient,
        dialog_repo: MaxDialogRepo,
        mid_registry: MaxMidRegistry,
        flow_message_storage: IFlowMessageStorage | None = None,
        ensure_user_middleware: MaxEnsureUserMiddleware | None = None,
    ) -> None:
        self.flow_message_storage = flow_message_storage
        self.ensure_user_middleware = ensure_user_middleware
        self.api_client = api_client
        self.dialog_repo = dialog_repo
        self._mid_registry = mid_registry

    def setup(
        self,
        messenger: MaxMessenger,
        callback_answerer: MaxCallbackAnswerer,
        callback_handler_registry: MaxCallbackHandlerRegistry,
        message_handler_registry: MaxMessageHandlerRegistry,
        next_step_registrar: MaxNextStepHandlerRegistrar,
        polling: MaxPolling,
    ) -> None:
        self.message_sender: MaxMessenger = messenger
        self.message_replacer: MaxMessenger = messenger
        self.message_deleter: MaxMessenger = messenger
        self.document_sender: MaxMessenger = messenger
        self.document_downloader: MaxMessenger = messenger
        self.callback_answerer: MaxCallbackAnswerer = callback_answerer
        self.callback_handler_registry: MaxCallbackHandlerRegistry = callback_handler_registry
        self.message_handler_registry: MaxMessageHandlerRegistry = message_handler_registry
        self._next_step_registrar: MaxNextStepHandlerRegistrar = next_step_registrar
        self._polling: MaxPolling = polling

    @property
    def next_step_registrar(self) -> MaxNextStepHandlerRegistrar:
        return self._next_step_registrar

    @property
    def mid_to_int(self) -> dict[str, int]:
        return self._mid_registry.mid_to_int

    def register_mid(self, mid: str) -> int:
        return self._mid_registry.register_mid(mid)

    def int_to_mid(self, int_id: int) -> str:
        return self._mid_registry.int_to_mid(int_id)

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

    def create_bot_message(self, chat_id: int, msg: dict[str, Any]) -> BotMessage:
        body = msg.get("body") or msg.get("message") or {}
        raw_mid = body.get("mid", "")
        message_id = self.register_mid(raw_mid) if raw_mid else 0

        sender = msg.get("sender", {})
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
