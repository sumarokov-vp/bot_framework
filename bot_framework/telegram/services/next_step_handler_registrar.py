from __future__ import annotations

from typing import TYPE_CHECKING

from telebot.types import Message

from bot_framework.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.protocols.i_message_handler import IMessageHandler

if TYPE_CHECKING:
    from .telegram_message_core import TelegramMessageCore


class NextStepHandlerRegistrar:
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core

    def register(
        self,
        message: BotMessage,
        handler: IMessageHandler,
    ) -> None:
        def wrapper(msg: Message) -> bool | None:
            bot_msg = self._to_bot_message(msg)
            return handler.handle(bot_msg)

        self._core.bot.register_next_step_handler(
            message.get_original(),
            wrapper,
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
