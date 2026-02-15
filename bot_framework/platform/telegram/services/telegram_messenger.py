from __future__ import annotations

from io import BytesIO
from logging import getLogger
from typing import TYPE_CHECKING

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.parse_mode import ParseMode

if TYPE_CHECKING:
    from .telegram_message_core import TelegramMessageCore


class TelegramMessenger:
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core
        self._logger = getLogger(__name__)

    def send(
        self,
        chat_id: int,
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
            msg = self._core.bot.send_message(
                chat_id=chat_id,
                text=text_to_send,
                parse_mode=self._core.convert_parse_mode(parse_mode),
                reply_markup=reply_markup,
            )
        except Exception as er:
            self._logger.error("Failed to send message", exc_info=er)
            msg = self._core.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
            )
        try:
            self._core.register_message(chat_id, msg.message_id, flow_name)
        except Exception as er:
            self._logger.error("Failed to register message", exc_info=er)
        return self._core.create_bot_message(chat_id, msg)

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        html_text = self._core.convert_markdown_to_html(text)
        return self.send(chat_id, html_text, ParseMode.HTML, keyboard, flow_name)

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
                parse_mode=self._core.convert_parse_mode(parse_mode),
                reply_markup=reply_markup,
            )
            self._core.register_message(chat_id, message_id, flow_name)
            return self._core.create_bot_message(chat_id, msg)
        except Exception as er:
            if "message is not modified" in str(er):
                self._logger.debug("Message content unchanged, skipping edit")
                return BotMessage(chat_id=chat_id, message_id=message_id)
            self._logger.error("Failed to replace message", exc_info=er)
            raise

    def delete(self, chat_id: int, message_id: int) -> None:
        try:
            self._core.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as er:
            self._logger.warning("Failed to delete message", exc_info=er)

    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage:
        reply_markup = self._core.convert_keyboard(keyboard) if keyboard else None
        file_obj = BytesIO(document)
        file_obj.name = filename
        msg = self._core.bot.send_document(
            chat_id=chat_id,
            document=file_obj,
            reply_markup=reply_markup,
        )
        return self._core.create_bot_message(chat_id, msg)

    def download_document(self, file_id: str) -> bytes:
        file_info = self._core.bot.get_file(file_id)
        return self._core.bot.download_file(file_info.file_path)
