from typing import Protocol

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.protocols.i_message_handler import IMessageHandler


class INextStepHandlerRegistrar(Protocol):
    def register(
        self,
        message: BotMessage,
        handler: IMessageHandler,
    ) -> None: ...
