from __future__ import annotations

from collections.abc import Callable
from logging import getLogger
from typing import Any

from bot_framework.core.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.core.protocols.i_message_handler import IMessageHandler


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


class MaxMessageHandlerRegistry:
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

    def dispatch(
        self,
        update: dict[str, Any],
        mid_to_int: dict[str, int],
        command_override: str | None = None,
    ) -> None:
        bot_message = self._to_bot_message(update, mid_to_int, command_override)
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

    def _to_bot_message(
        self,
        update: dict[str, Any],
        mid_to_int: dict[str, int],
        command_override: str | None,
    ) -> BotMessage:
        message = update.get("message", {})
        sender = message.get("sender", {})
        recipient = message.get("recipient", {})
        body = message.get("body", {}) or message.get("message", {})

        user_id = int(sender.get("user_id", 0))
        chat_id_raw = recipient.get("chat_id") or recipient.get("user_id")
        chat_id = int(chat_id_raw) if chat_id_raw is not None else user_id

        raw_mid = body.get("mid", "")
        message_id = mid_to_int.get(raw_mid, hash(raw_mid) & 0x7FFFFFFF)

        text = command_override or body.get("text")

        from_user = BotMessageUser(id=user_id)
        bot_message = BotMessage(
            chat_id=chat_id,
            message_id=message_id,
            user_id=user_id,
            text=text,
            from_user=from_user,
        )
        bot_message.set_original(update)
        return bot_message
