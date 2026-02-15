from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telebot import TeleBot


class TelegramForumTopicCreator:
    def __init__(self, bot: TeleBot) -> None:
        self._bot = bot

    def create_topic(self, chat_id: int, name: str) -> int:
        result = self._bot.create_forum_topic(chat_id=chat_id, name=name)
        return result.message_thread_id
