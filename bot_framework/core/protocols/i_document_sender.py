from typing import Protocol

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard


class IDocumentSender(Protocol):
    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage: ...
