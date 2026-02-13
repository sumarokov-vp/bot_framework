from typing import Protocol

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.parse_mode import ParseMode


class IMessageSender(Protocol):
    def send(
        self,
        chat_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage: ...

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage: ...

    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage: ...

    def download_document(self, file_id: str) -> bytes: ...
