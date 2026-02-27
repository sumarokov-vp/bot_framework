from __future__ import annotations

from typing import Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.protocols.i_message_handler import IMessageHandler
from bot_framework.platform.max.services.max_bot_message_factory import MaxBotMessageFactory


class MaxNextStepHandlerRegistrar:
    def __init__(self) -> None:
        self._handlers: dict[int, IMessageHandler] = {}

    def register(
        self,
        message: BotMessage,
        handler: IMessageHandler,
    ) -> None:
        self._handlers[message.user_id] = handler

    def pop(self, user_id: int) -> IMessageHandler | None:
        return self._handlers.pop(user_id, None)

    def to_bot_message(
        self,
        update: dict[str, Any],
        mid_to_int: dict[str, int],
    ) -> BotMessage:
        return MaxBotMessageFactory.from_update(update, mid_to_int)
