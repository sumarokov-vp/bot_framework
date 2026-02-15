from __future__ import annotations

from typing import Any, Protocol

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard

from .i_callback_answerer import ICallbackAnswerer
from .i_callback_answerer_bot import ICallbackAnswererBot
from .i_callback_handler_registrar_bot import ICallbackHandlerRegistrarBot
from .i_callback_handler_registry import ICallbackHandlerRegistry
from .i_document_downloader import IDocumentDownloader
from .i_document_sender import IDocumentSender
from .i_file_downloader_bot import IFileDownloaderBot
from .i_message_deleter import IMessageDeleter
from .i_message_forwarder import IMessageForwarder
from .i_message_handler_registrar_bot import IMessageHandlerRegistrarBot
from .i_message_handler_registry import IMessageHandlerRegistry
from .i_message_replacer import IMessageReplacer
from .i_message_sender import IMessageSender
from .i_message_sender_bot import IMessageSenderBot
from .i_middleware_setup import IMiddlewareSetup
from .i_next_step_handler_registrar import INextStepHandlerRegistrar
from .i_next_step_handler_registrar_bot import INextStepHandlerRegistrarBot
from .i_polling_bot import IPollingBot
from .i_raw_forum_topic_creator import IRawForumTopicCreator
from .i_thread_message_sender import IThreadMessageSender


class IMessageCore(Protocol):
    @property
    def message_sender_bot(self) -> IMessageSenderBot: ...

    @property
    def file_downloader_bot(self) -> IFileDownloaderBot: ...

    @property
    def callback_answerer_bot(self) -> ICallbackAnswererBot: ...

    @property
    def callback_handler_registrar_bot(self) -> ICallbackHandlerRegistrarBot: ...

    @property
    def message_handler_registrar_bot(self) -> IMessageHandlerRegistrarBot: ...

    @property
    def next_step_handler_registrar_bot(self) -> INextStepHandlerRegistrarBot: ...

    @property
    def polling_bot(self) -> IPollingBot: ...

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

    @property
    def raw_forum_topic_creator(self) -> IRawForumTopicCreator: ...

    @property
    def thread_message_sender(self) -> IThreadMessageSender: ...

    @property
    def message_forwarder(self) -> IMessageForwarder: ...

    @property
    def middleware_setup(self) -> IMiddlewareSetup: ...

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
