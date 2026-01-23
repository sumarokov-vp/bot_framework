from __future__ import annotations

from typing import TYPE_CHECKING

from telebot.types import CallbackQuery

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.protocols.i_callback_handler import ICallbackHandler

if TYPE_CHECKING:
    from .telegram_message_core import TelegramMessageCore


class CallbackHandlerRegistry:
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core

    def register(self, handler: ICallbackHandler) -> None:
        def wrapper(call: CallbackQuery) -> None:
            bot_callback = self._to_bot_callback(call)
            handler.handle(bot_callback)

        self._core.bot.register_callback_query_handler(
            wrapper,
            func=lambda call: call.data and call.data.startswith(handler.prefix),
        )

    def _to_bot_callback(self, call: CallbackQuery) -> BotCallback:
        if not call.from_user:
            raise ValueError("call.from_user is required but was None")

        message_id: int | None = None
        message_chat_id: int | None = None
        if call.message:
            message_id = call.message.message_id
            message_chat_id = call.message.chat.id

        bot_callback = BotCallback(
            id=str(call.id),
            user_id=call.from_user.id,
            data=call.data,
            message_id=message_id,
            message_chat_id=message_chat_id,
            user_language_code=call.from_user.language_code,
        )
        bot_callback.set_original(call)
        return bot_callback
