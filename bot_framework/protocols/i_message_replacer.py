from typing import Protocol

from bot_framework.entities.bot_message import BotMessage
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.parse_mode import ParseMode


class IMessageReplacer(Protocol):
    def replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage: ...
