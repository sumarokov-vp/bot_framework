from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.features.menus.language_menu.i_language_menu_sender import (
    ILanguageMenuSender,
)
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class LanguageCommandHandler:
    def __init__(
        self,
        language_menu_sender: ILanguageMenuSender,
        user_repo: IUserRepo,
    ) -> None:
        self.language_menu_sender = language_menu_sender
        self.user_repo = user_repo
        self.allowed_roles: set[str] | None = None

    def handle(self, message: BotMessage) -> None:
        if message.user_id is None:
            return
        user = self.user_repo.get_by_id(id=message.user_id)
        if not user:
            return
        self.language_menu_sender.send(user)
