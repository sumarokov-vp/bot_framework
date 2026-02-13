from __future__ import annotations

from typing import TYPE_CHECKING

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.parse_mode import ParseMode
from bot_framework.protocols.i_message_service import IMessageService

if TYPE_CHECKING:
    from .telegram_message_deleter import TelegramMessageDeleter
    from .telegram_message_replacer import TelegramMessageReplacer
    from .telegram_message_sender import TelegramMessageSender
    from .telegram_notify_replacer import TelegramNotifyReplacer


class TelegramMessageService(IMessageService):
    def __init__(
        self,
        sender: TelegramMessageSender,
        replacer: TelegramMessageReplacer,
        deleter: TelegramMessageDeleter,
        notify_replacer: TelegramNotifyReplacer,
    ) -> None:
        self._sender = sender
        self._replacer = replacer
        self._deleter = deleter
        self._notify_replacer = notify_replacer

    def send(
        self,
        chat_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        return self._sender.send(chat_id, text, parse_mode, keyboard, flow_name)

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        return self._sender.send_markdown_as_html(chat_id, text, keyboard, flow_name)

    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage:
        return self._sender.send_document(chat_id, document, filename, keyboard)

    def download_document(self, file_id: str) -> bytes:
        return self._sender.download_document(file_id)

    def replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        return self._replacer.replace(
            chat_id, message_id, text, parse_mode, keyboard, flow_name
        )

    def delete(self, chat_id: int, message_id: int) -> None:
        self._deleter.delete(chat_id, message_id)

    def notify_replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        return self._notify_replacer.notify_replace(
            chat_id, message_id, text, parse_mode, keyboard, flow_name
        )
