from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.features.flows.request_role_flow.protocols import (
    IRequestRoleFlowRouter,
)
from bot_framework.core.protocols.i_message_handler import IMessageHandler
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class RequestRoleCommandHandler(IMessageHandler):
    allowed_roles: set[str] | None = None

    def __init__(
        self,
        request_role_flow_router: IRequestRoleFlowRouter,
        user_repo: IUserRepo,
    ) -> None:
        self.request_role_flow_router = request_role_flow_router
        self.user_repo = user_repo

    def handle(self, message: BotMessage) -> None:
        if not message.from_user:
            raise ValueError("message.from_user is required but was None")

        user = self.user_repo.get_by_id(id=message.from_user.id)
        self.request_role_flow_router.start(user)
