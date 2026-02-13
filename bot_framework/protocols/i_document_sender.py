from typing import Protocol

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard


class IDocumentSender(Protocol):
    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage: ...
