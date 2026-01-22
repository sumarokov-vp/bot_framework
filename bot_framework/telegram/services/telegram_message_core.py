from __future__ import annotations

from telebot import TeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.flow_management import IFlowMessageStorage

from .markdown_escaper import MarkdownEscaper
from .markdown_to_html_converter import MarkdownToHtmlConverter


class TelegramMessageCore:
    def __init__(
        self,
        bot: TeleBot,
        flow_message_storage: IFlowMessageStorage | None = None,
    ) -> None:
        self.bot = bot
        self.flow_message_storage = flow_message_storage
        self._markdown_escaper = MarkdownEscaper()
        self._markdown_to_html_converter = MarkdownToHtmlConverter()

    def register_message(
        self,
        chat_id: int,
        message_id: int,
        flow_name: str | None,
    ) -> None:
        if flow_name and self.flow_message_storage:
            self.flow_message_storage.add_message(
                telegram_id=chat_id,
                flow_name=flow_name,
                message_id=message_id,
            )

    def create_bot_message(self, chat_id: int, msg: object) -> BotMessage:
        bot_message = BotMessage(chat_id=chat_id, message_id=msg.message_id)  # type: ignore[attr-defined]
        bot_message.set_original(msg)
        return bot_message

    def convert_keyboard(self, keyboard: Keyboard) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for row in keyboard.rows:
            buttons = [
                InlineKeyboardButton(
                    text=button.text, callback_data=button.callback_data
                )
                for button in row
            ]
            markup.row(*buttons)
        return markup

    def escape_markdown(self, text: str) -> str:
        return self._markdown_escaper.escape(text)

    def convert_markdown_to_html(self, text: str) -> str:
        return self._markdown_to_html_converter.convert(text)
