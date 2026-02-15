from uuid import uuid4

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.features.menus.language_menu.i_language_menu_sender import ILanguageMenuSender
from bot_framework.core.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class ShowLanguageMenuHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        language_menu_sender: ILanguageMenuSender,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.language_menu_sender = language_menu_sender
        self.user_repo = user_repo
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        user = self.user_repo.get_by_id(id=callback.user_id)
        self.language_menu_sender.send(user)
