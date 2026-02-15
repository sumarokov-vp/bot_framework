from uuid import uuid4

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.features.menus.language_menu.i_language_menu_sender import ILanguageMenuSender
from bot_framework.core.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class SelectLanguageHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.user_repo = user_repo
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None
        self._language_menu_sender: ILanguageMenuSender | None = None

    def set_language_menu_sender(self, sender: ILanguageMenuSender) -> None:
        self._language_menu_sender = sender

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.data:
            raise ValueError("callback.data is required but was None")

        parts = callback.data.split(":")
        if len(parts) < 2:
            raise ValueError(f"Invalid callback data format: {callback.data}")

        new_language_code = parts[1]

        self.user_repo.update_language(
            user_id=callback.user_id,
            language_code=new_language_code,
        )

        user = self.user_repo.get_by_id(callback.user_id)
        if not user:
            raise ValueError(f"User not found: {callback.user_id}")

        if not callback.message_id:
            raise ValueError("callback.message_id is required but was None")

        if not self._language_menu_sender:
            raise ValueError("language_menu_sender is not set")

        self._language_menu_sender.replace(user=user, message_id=callback.message_id)
