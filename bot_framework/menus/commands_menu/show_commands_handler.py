from uuid import uuid4

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.menus.commands_menu.i_commands_menu_sender import ICommandsMenuSender
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class ShowCommandsHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        commands_menu_sender: ICommandsMenuSender,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.commands_menu_sender = commands_menu_sender
        self.user_repo = user_repo
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        user = self.user_repo.get_by_id(id=callback.user_id)
        self.commands_menu_sender.send(user)
