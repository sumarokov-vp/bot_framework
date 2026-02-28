from __future__ import annotations

from logging import getLogger
from typing import Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.protocols.i_message_handler import IMessageHandler
from bot_framework.platform.max.services.max_bot_message_factory import MaxBotMessageFactory

logger = getLogger(__name__)


class MaxNextStepHandlerRegistrar:
    def __init__(self) -> None:
        self._handlers: dict[int, IMessageHandler] = {}

    def register(
        self,
        message: BotMessage,
        handler: IMessageHandler,
    ) -> None:
        logger.info(
            "register next_step: chat_id=%s handler=%s",
            message.chat_id,
            type(handler).__name__,
        )
        self._handlers[message.chat_id] = handler

    def pop(self, chat_id: int) -> IMessageHandler | None:
        handler = self._handlers.pop(chat_id, None)
        logger.info(
            "pop next_step: chat_id=%s found=%s",
            chat_id, type(handler).__name__ if handler else None,
        )
        return handler

    def to_bot_message(
        self,
        update: dict[str, Any],
        mid_to_int: dict[str, int],
    ) -> BotMessage:
        return MaxBotMessageFactory.from_update(update, mid_to_int)
