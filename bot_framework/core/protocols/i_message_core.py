from __future__ import annotations

from typing import Any, Protocol

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard

from .i_callback_answerer import ICallbackAnswerer
from .i_callback_handler_registry import ICallbackHandlerRegistry
from .i_document_downloader import IDocumentDownloader
from .i_document_sender import IDocumentSender
from .i_message_deleter import IMessageDeleter
from .i_message_handler_registry import IMessageHandlerRegistry
from .i_message_replacer import IMessageReplacer
from .i_message_sender import IMessageSender
from .i_next_step_handler_registrar import INextStepHandlerRegistrar
from .i_bot import IBot


class IMessageCore(Protocol):
    @property
    def bot(self) -> IBot: ...

    @property
    def message_sender(self) -> IMessageSender: ...

    @property
    def message_replacer(self) -> IMessageReplacer: ...

    @property
    def message_deleter(self) -> IMessageDeleter: ...

    @property
    def document_sender(self) -> IDocumentSender: ...

    @property
    def document_downloader(self) -> IDocumentDownloader: ...

    @property
    def callback_handler_registry(self) -> ICallbackHandlerRegistry: ...

    @property
    def message_handler_registry(self) -> IMessageHandlerRegistry: ...

    @property
    def callback_answerer(self) -> ICallbackAnswerer: ...

    @property
    def next_step_registrar(self) -> INextStepHandlerRegistrar: ...

    def register_message(
        self,
        chat_id: int,
        message_id: int,
        flow_name: str | None,
    ) -> None: ...

    def create_bot_message(self, chat_id: int, msg: Any) -> BotMessage: ...

    def convert_keyboard(self, keyboard: Keyboard) -> Any: ...

    def escape_markdown(self, text: str) -> str: ...

    def convert_markdown_to_html(self, text: str) -> str: ...
