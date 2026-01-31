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
    from .telegram_message_service import TelegramMessageService

TELEGRAM_PARSE_MODE_MAP: dict[ParseMode, str | None] = {
    ParseMode.HTML: "HTML",
    ParseMode.MARKDOWN: "MarkdownV2",
    ParseMode.PLAIN: None,
}


class TelegramMessageCore:
    def __init__(
        self,
        bot_token: str,
        database_url: str | None = None,
        flow_message_storage: IFlowMessageStorage | None = None,
        use_class_middlewares: bool = True,
    ) -> None:
        self.bot = TeleBot(token=bot_token, use_class_middlewares=use_class_middlewares)
        self.flow_message_storage = flow_message_storage
        self._markdown_escaper = MarkdownEscaper()
        self._markdown_to_html_converter = MarkdownToHtmlConverter()
        self._init_components()

        if database_url:
            self._setup_ensure_user_middleware(database_url)

    def _setup_ensure_user_middleware(self, database_url: str) -> None:
        from bot_framework.role_management.repos import RoleRepo, UserRepo
        from bot_framework.role_management.services import EnsureUserExists
        from bot_framework.telegram.middleware import EnsureUserMiddleware

        user_repo = UserRepo(database_url=database_url)
        role_repo = RoleRepo(database_url=database_url)
        ensure_user_exists = EnsureUserExists(
            user_repo=user_repo,
            role_repo=role_repo,
        )
        middleware = EnsureUserMiddleware(ensure_user_exists=ensure_user_exists)
        self.bot.setup_middleware(middleware)

    def _init_components(self) -> None:
        from .callback_answerer import CallbackAnswerer
        from .callback_handler_registry import CallbackHandlerRegistry
        from .message_handler_registry import MessageHandlerRegistry
        from .next_step_handler_registrar import NextStepHandlerRegistrar
        from .telegram_message_deleter import TelegramMessageDeleter
        from .telegram_message_replacer import TelegramMessageReplacer
        from .telegram_message_sender import TelegramMessageSender
        from .telegram_message_service import TelegramMessageService
        from .telegram_notify_replacer import TelegramNotifyReplacer

        self.message_sender: TelegramMessageSender = TelegramMessageSender(self)
        self.message_replacer: TelegramMessageReplacer = TelegramMessageReplacer(self)
        self.message_deleter: TelegramMessageDeleter = TelegramMessageDeleter(self)

        notify_replacer = TelegramNotifyReplacer(
            sender=self.message_sender,
            deleter=self.message_deleter,
        )
        self.message_service: TelegramMessageService = TelegramMessageService(
            sender=self.message_sender,
            replacer=self.message_replacer,
            deleter=self.message_deleter,
            notify_replacer=notify_replacer,
        )

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
