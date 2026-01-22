from typing import Protocol

from bot_framework.entities.bot_message import BotMessageUser


class IRequestRoleFlowRouter(Protocol):
    def start(self, user: BotMessageUser, chat_id: int) -> None: ...
