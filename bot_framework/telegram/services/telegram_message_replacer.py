from __future__ import annotations

from logging import getLogger

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.parse_mode import ParseMode
from bot_framework.protocols.i_message_replacer import IMessageReplacer

from .telegram_message_core import TelegramMessageCore


class TelegramMessageReplacer(IMessageReplacer):
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core
        self._logger = getLogger(__name__)

    def replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        reply_markup = self._core.convert_keyboard(keyboard) if keyboard else None
        text_to_send = text
        if parse_mode == ParseMode.MARKDOWN:
            text_to_send = self._core.escape_markdown(text)
        try:
            msg = self._core.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text_to_send,
                parse_mode=parse_mode.value,
                reply_markup=reply_markup,
            )
            self._core.register_message(chat_id, message_id, flow_name)
            return self._core.create_bot_message(chat_id, msg)
        except Exception as er:
            if "message is not modified" in str(er):
                self._logger.debug("Message content unchanged, skipping edit")
                bot_message = BotMessage(chat_id=chat_id, message_id=message_id)
                return bot_message
            self._logger.error("Failed to replace message", exc_info=er)
            raise
