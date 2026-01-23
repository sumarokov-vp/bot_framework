from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from bot_framework.protocols.i_message_deleter import IMessageDeleter

if TYPE_CHECKING:
    from .telegram_message_core import TelegramMessageCore


class TelegramMessageDeleter(IMessageDeleter):
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core
        self._logger = getLogger(__name__)

    def delete(self, chat_id: int, message_id: int) -> None:
        try:
            self._core.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as er:
            self._logger.warning("Failed to delete message", exc_info=er)
