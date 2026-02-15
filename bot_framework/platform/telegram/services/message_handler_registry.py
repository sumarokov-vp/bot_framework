from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from telebot.types import Message

from bot_framework.core.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.core.protocols.i_message_handler import IMessageHandler

if TYPE_CHECKING:
    from .telegram_message_core import TelegramMessageCore


class MessageHandlerRegistry:
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core

    def register(
        self,
        handler: IMessageHandler,
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[[Message], bool] | None = None,
    ) -> None:
        def wrapper(message: Message) -> bool | None:
            bot_message = self._to_bot_message(message)
            return handler.handle(bot_message)

        self._core.message_handler_registrar_bot.register_message_handler(
            callback=wrapper,
            commands=commands,
            content_types=content_types,
            func=func,
        )

    def _to_bot_message(self, message: Message) -> BotMessage:
        if not message.from_user:
            raise ValueError("message.from_user is required but was None")

        from_user = BotMessageUser(
            id=message.from_user.id,
        )

        bot_message = BotMessage(
            chat_id=message.chat.id,
            message_id=message.message_id,
            user_id=message.from_user.id,
            text=message.text,
            from_user=from_user,
        )
        bot_message.set_original(message)
        return bot_message
