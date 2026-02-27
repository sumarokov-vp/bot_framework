from __future__ import annotations

from typing import Protocol

from .i_callback_answerer_bot import ICallbackAnswererBot
from .i_callback_handler_registrar_bot import ICallbackHandlerRegistrarBot
from .i_file_downloader_bot import IFileDownloaderBot
from .i_message_core_base import IMessageCoreBase
from .i_message_forwarder import IMessageForwarder
from .i_message_handler_registrar_bot import IMessageHandlerRegistrarBot
from .i_message_sender_bot import IMessageSenderBot
from .i_middleware_setup import IMiddlewareSetup
from .i_next_step_handler_registrar_bot import INextStepHandlerRegistrarBot
from .i_polling_bot import IPollingBot
from .i_raw_forum_topic_creator import IRawForumTopicCreator
from .i_thread_message_sender import IThreadMessageSender


class IMessageCore(IMessageCoreBase, Protocol):
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
    def raw_forum_topic_creator(self) -> IRawForumTopicCreator: ...

    @property
    def thread_message_sender(self) -> IThreadMessageSender: ...

    @property
    def message_forwarder(self) -> IMessageForwarder: ...

    @property
    def middleware_setup(self) -> IMiddlewareSetup: ...

    def escape_markdown(self, text: str) -> str: ...

    def convert_markdown_to_html(self, text: str) -> str: ...
