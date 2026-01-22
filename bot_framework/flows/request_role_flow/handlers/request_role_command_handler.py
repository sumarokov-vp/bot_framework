from bot_framework.entities.bot_message import BotMessage
from bot_framework.flows.request_role_flow.protocols import (
    IRequestRoleFlowRouter,
)
from bot_framework.protocols.i_message_handler import IMessageHandler


class RequestRoleCommandHandler(IMessageHandler):
    allowed_roles: set[str] | None = None

    def __init__(
        self,
        request_role_flow_router: IRequestRoleFlowRouter,
    ) -> None:
        self.request_role_flow_router = request_role_flow_router

    def handle(self, message: BotMessage) -> None:
        if not message.from_user:
            raise ValueError("message.from_user is required but was None")

        self.request_role_flow_router.start(
            user=message.from_user,
            chat_id=message.chat_id,
        )
