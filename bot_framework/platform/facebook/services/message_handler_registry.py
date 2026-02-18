from __future__ import annotations

from collections.abc import Callable
from logging import getLogger

from bot_framework.core.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.core.protocols.i_message_handler import IMessageHandler
from bot_framework.platform.facebook.entities.webhook_event import WebhookEvent


class _RegisteredHandler:
    def __init__(
        self,
        handler: IMessageHandler,
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[..., bool] | None = None,
    ) -> None:
        self.handler = handler
        self.commands = commands
        self.content_types = content_types
        self.func = func


class FacebookMessageHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: list[_RegisteredHandler] = []
        self._logger = getLogger(__name__)

    def register(
        self,
        handler: IMessageHandler,
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[..., bool] | None = None,
    ) -> None:
        self._handlers.append(_RegisteredHandler(handler, commands, content_types, func))

    def handle_event(self, event: WebhookEvent) -> None:
        if not event.message:
            return
        if event.message.quick_reply:
            return

        bot_message = self._to_bot_message(event)

        for registered in self._handlers:
            if self._matches(registered, bot_message):
                registered.handler.handle(bot_message)
                return

    def _matches(self, registered: _RegisteredHandler, message: BotMessage) -> bool:
        if registered.commands and message.text:
            text = message.text.strip()
            for cmd in registered.commands:
                if text == f"/{cmd}" or text.lower() == cmd.lower():
                    return True
            return False

        if registered.content_types:
            return True

        if registered.func:
            return registered.func(message)

        if not registered.commands and not registered.content_types and not registered.func:
            return True

        return False

    def _to_bot_message(self, event: WebhookEvent) -> BotMessage:
        sender_id = int(event.sender.id)
        message = event.message
        if not message:
            raise ValueError("event.message is required but was None")

        from_user = BotMessageUser(id=sender_id)
        bot_message = BotMessage(
            chat_id=sender_id,
            message_id=hash(message.mid),
            user_id=sender_id,
            text=message.text,
            from_user=from_user,
        )
        bot_message.set_original(event)
        return bot_message
