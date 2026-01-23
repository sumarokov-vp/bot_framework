from __future__ import annotations

from typing import TYPE_CHECKING

from telebot import TeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.parse_mode import ParseMode
from bot_framework.flow_management import IFlowMessageStorage

from .markdown_escaper import MarkdownEscaper
from .markdown_to_html_converter import MarkdownToHtmlConverter

if TYPE_CHECKING:
    from .callback_answerer import CallbackAnswerer
    from .callback_handler_registry import CallbackHandlerRegistry
    from .message_handler_registry import MessageHandlerRegistry
    from .next_step_handler_registrar import NextStepHandlerRegistrar
    from .telegram_message_deleter import TelegramMessageDeleter
    from .telegram_message_replacer import TelegramMessageReplacer
    from .telegram_message_sender import TelegramMessageSender

TELEGRAM_PARSE_MODE_MAP: dict[ParseMode, str | None] = {
    ParseMode.HTML: "HTML",
    ParseMode.MARKDOWN: "MarkdownV2",
    ParseMode.PLAIN: None,
}


class TelegramMessageCore:
    def __init__(
        self,
        bot_token: str,
        flow_message_storage: IFlowMessageStorage | None = None,
        use_class_middlewares: bool = False,
    ) -> None:
        self.bot = TeleBot(token=bot_token, use_class_middlewares=use_class_middlewares)
        self.flow_message_storage = flow_message_storage
        self._markdown_escaper = MarkdownEscaper()
        self._markdown_to_html_converter = MarkdownToHtmlConverter()
        self._init_components()

    def _init_components(self) -> None:
        from .callback_answerer import CallbackAnswerer
        from .callback_handler_registry import CallbackHandlerRegistry
        from .message_handler_registry import MessageHandlerRegistry
        from .next_step_handler_registrar import NextStepHandlerRegistrar
        from .telegram_message_deleter import TelegramMessageDeleter
        from .telegram_message_replacer import TelegramMessageReplacer
        from .telegram_message_sender import TelegramMessageSender

        self.message_sender: TelegramMessageSender = TelegramMessageSender(self)
        self.message_replacer: TelegramMessageReplacer = TelegramMessageReplacer(self)
        self.message_deleter: TelegramMessageDeleter = TelegramMessageDeleter(self)
        self.callback_handler_registry: CallbackHandlerRegistry = (
            CallbackHandlerRegistry(self)
        )
        self.message_handler_registry: MessageHandlerRegistry = MessageHandlerRegistry(
            self
        )
        self.callback_answerer: CallbackAnswerer = CallbackAnswerer(self)
        self.next_step_registrar: NextStepHandlerRegistrar = NextStepHandlerRegistrar(
            self
        )

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

    def convert_parse_mode(self, parse_mode: ParseMode) -> str | None:
        return TELEGRAM_PARSE_MODE_MAP.get(parse_mode)
