from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard

if TYPE_CHECKING:
    from bot_framework.domain.flow_management.protocols.i_flow_message_storage import (
        IFlowMessageStorage,
    )

from .facebook_api_client import FacebookApiClient
from .facebook_callback_answerer import FacebookCallbackAnswerer
from .facebook_messenger import FacebookMessenger
from .facebook_notify_replacer import FacebookNotifyReplacer
from .facebook_webhook_server import FacebookWebhookServer
from .message_handler_registry import FacebookMessageHandlerRegistry
from .postback_handler_registry import PostbackHandlerRegistry


class FacebookMessageCore:
    def __init__(
        self,
        page_access_token: str,
        verify_token: str,
        flow_message_storage: IFlowMessageStorage | None = None,
    ) -> None:
        self.flow_message_storage = flow_message_storage
        self.api_client = FacebookApiClient(page_access_token)
        self._init_components()
        self._webhook_server = FacebookWebhookServer(
            verify_token=verify_token,
            postback_registry=self.callback_handler_registry,
            message_registry=self.message_handler_registry,
        )

    def _init_components(self) -> None:
        messenger = FacebookMessenger(self)
        self.message_sender: FacebookMessenger = messenger
        self.message_deleter: FacebookMessenger = messenger

        self.message_replacer: FacebookNotifyReplacer = FacebookNotifyReplacer(
            sender=messenger,
            deleter=messenger,
        )

        self.notify_replacer: FacebookNotifyReplacer = FacebookNotifyReplacer(
            sender=messenger,
            deleter=messenger,
        )

        self.callback_handler_registry: PostbackHandlerRegistry = PostbackHandlerRegistry()
        self.message_handler_registry: FacebookMessageHandlerRegistry = (
            FacebookMessageHandlerRegistry()
        )
        self.callback_answerer: FacebookCallbackAnswerer = FacebookCallbackAnswerer()

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

    def create_bot_message(self, chat_id: int, msg: Any) -> BotMessage:
        return BotMessage(
            chat_id=chat_id,
            message_id=hash(str(msg)),
        )

    def convert_keyboard(self, keyboard: Keyboard) -> dict[str, Any]:
        messenger = FacebookMessenger(self)
        return messenger._build_message_payload("", keyboard)

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:  # noqa: S104
        self._webhook_server.run(host=host, port=port)

    @property
    def webhook_app(self) -> Any:
        return self._webhook_server.app
