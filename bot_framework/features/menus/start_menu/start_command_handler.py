from bot_framework.domain.decorators.role_checker import check_message_roles
from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.features.flows.request_role_flow.protocols import (
    IRequestRoleFlowRouter,
)
from bot_framework.features.menus.start_menu.i_main_menu_sender import IMainMenuSender
from bot_framework.core.protocols.i_message_handler import IMessageHandler
from bot_framework.core.protocols.i_message_sender import IMessageSender
from bot_framework.domain.role_management.repos.protocols.i_role_repo import IRoleRepo
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class StartCommandHandler(IMessageHandler):
    allowed_roles: set[str] | None = None

    def __init__(
        self,
        user_repo: IUserRepo,
        role_repo: IRoleRepo,
        main_menu_sender: IMainMenuSender,
        request_role_flow_router: IRequestRoleFlowRouter,
        message_sender: IMessageSender | None = None,
    ) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.main_menu_sender = main_menu_sender
        self.request_role_flow_router = request_role_flow_router
        self.message_sender = message_sender

    @check_message_roles
    def handle(self, message: BotMessage) -> None:
        if not message.from_user:
            raise ValueError("message.from_user is required but was None")

        user = self.user_repo.get_by_id(id=message.from_user.id)

        user_roles = self.role_repo.get_user_roles(user_id=user.id)
        if not user_roles:
            self.request_role_flow_router.start(user)
            return

        self.main_menu_sender.send(user)
