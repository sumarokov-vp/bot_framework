from __future__ import annotations

from logging import getLogger

from telebot import TeleBot

from bot_framework.protocols.i_message_deleter import IMessageDeleter


class TelegramMessageDeleter(IMessageDeleter):
    def __init__(self, bot: TeleBot) -> None:
        self._bot = bot
        self._logger = getLogger(__name__)

    def delete(self, chat_id: int, message_id: int) -> None:
        try:
            self._bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as er:
            self._logger.warning("Failed to delete message", exc_info=er)
