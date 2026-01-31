from __future__ import annotations

from logging import getLogger

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.parse_mode import ParseMode
from bot_framework.protocols.i_message_sender import IMessageSender

from .telegram_message_core import TelegramMessageCore


class TelegramMessageSender(IMessageSender):
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

    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
    ) -> BotMessage:
        from io import BytesIO

        file_obj = BytesIO(document)
        file_obj.name = filename
        msg = self._core.bot.send_document(
            chat_id=chat_id,
            document=file_obj,
        )
        return self._core.create_bot_message(chat_id, msg)
