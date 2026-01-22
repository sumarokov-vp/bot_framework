from bot_framework.entities.bot_message import BotMessage
from bot_framework.flows.request_role_flow.protocols import IRequestRoleFlowRouter
from bot_framework.menus.start_menu.i_main_menu_sender import IMainMenuSender
from bot_framework.protocols.i_message_handler import IMessageHandler
from bot_framework.role_management.repos.protocols.i_role_repo import IRoleRepo
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class StartCommandHandler(IMessageHandler):
    allowed_roles: set[str] | None = None

    def __init__(
        self,
        user_repo: IUserRepo,
        role_repo: IRoleRepo,
        main_menu_sender: IMainMenuSender,
        request_role_flow_router: IRequestRoleFlowRouter,
    ) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.main_menu_sender = main_menu_sender
        self.request_role_flow_router = request_role_flow_router

    def handle(
        self,
        message: BotMessage,
    ) -> None:
        if not message.from_user:
            raise ValueError("message.from_user is required but was None")

        telegram_id = message.from_user.id

        user = self.user_repo.find_by_id(id=telegram_id)
        if not user:
            self.request_role_flow_router.start(
                user=message.from_user,
                chat_id=message.chat_id,
            )
            return

        user_roles = self.role_repo.get_user_roles(user_id=telegram_id)
        if not user_roles:
            self.request_role_flow_router.start(
                user=message.from_user,
                chat_id=message.chat_id,
            )
            return

        language_code = message.from_user.language_code or "en"
        self.main_menu_sender.send(message.chat_id, language_code)
