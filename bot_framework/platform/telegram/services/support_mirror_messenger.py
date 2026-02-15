from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.parse_mode import ParseMode

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_support_topic_manager import ISupportTopicManager
    from bot_framework.platform.telegram.services.telegram_messenger import TelegramMessenger
    from telebot import TeleBot


class SupportMirrorMessenger:
    def __init__(
        self,
        messenger: TelegramMessenger,
        bot: TeleBot,
        support_chat_id: int,
        support_topic_manager: ISupportTopicManager,
    ) -> None:
        self._messenger = messenger
        self._bot = bot
        self._support_chat_id = support_chat_id
        self._support_topic_manager = support_topic_manager
        self._logger = getLogger(__name__)

    def send(
        self,
        chat_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        result = self._messenger.send(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            keyboard=keyboard,
            flow_name=flow_name,
        )
        self._mirror_text(chat_id, text)
        return result

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        result = self._messenger.send_markdown_as_html(
            chat_id=chat_id,
            text=text,
            keyboard=keyboard,
            flow_name=flow_name,
        )
        self._mirror_text(chat_id, text)
        return result

    def replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        result = self._messenger.replace(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode,
            keyboard=keyboard,
            flow_name=flow_name,
        )
        self._mirror_text(chat_id, f"[edited] {text}")
        return result

    def delete(self, chat_id: int, message_id: int) -> None:
        self._messenger.delete(chat_id=chat_id, message_id=message_id)

    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage:
        result = self._messenger.send_document(
            chat_id=chat_id,
            document=document,
            filename=filename,
            keyboard=keyboard,
        )
        self._mirror_text(chat_id, f"[document] {filename}")
        return result

    def download_document(self, file_id: str) -> bytes:
        return self._messenger.download_document(file_id)

    def _mirror_text(self, chat_id: int, text: str) -> None:
        if chat_id == self._support_chat_id:
            return

        try:
            topic_id = self._support_topic_manager.ensure_topic(
                user_id=chat_id,
                full_name=str(chat_id),
            )
            self._bot.send_message(
                chat_id=self._support_chat_id,
                text=f"🤖 Бот:\n\n{text}",
                message_thread_id=topic_id,
            )
        except Exception as er:
            self._logger.error("Failed to mirror message to support chat", exc_info=er)
