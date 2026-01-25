from bot_framework.language_management.repos.protocols.i_language_repo import (
    ILanguageRepo,
)
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.menus.language_menu.language_menu_sender import LanguageMenuSender
from bot_framework.menus.language_menu.select_language_handler import (
    SelectLanguageHandler,
)
from bot_framework.menus.language_menu.show_language_menu_handler import (
    ShowLanguageMenuHandler,
)
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.protocols.i_callback_handler_registry import (
    ICallbackHandlerRegistry,
)
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class LanguageMenuFactory:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        language_repo: ILanguageRepo,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.language_repo = language_repo
        self.user_repo = user_repo

        self._show_language_menu_handler: ShowLanguageMenuHandler | None = None
        self._select_language_handler: SelectLanguageHandler | None = None

    def _get_select_language_handler(self) -> SelectLanguageHandler:
        if self._select_language_handler is None:
            self._select_language_handler = SelectLanguageHandler(
                callback_answerer=self.callback_answerer,
                message_sender=self.message_sender,
                phrase_repo=self.phrase_repo,
                user_repo=self.user_repo,
            )
        return self._select_language_handler

    def _get_show_language_menu_handler(self) -> ShowLanguageMenuHandler:
        if self._show_language_menu_handler is None:
            select_language_handler = self._get_select_language_handler()

            self._show_language_menu_handler = ShowLanguageMenuHandler(
                callback_answerer=self.callback_answerer,
                language_menu_sender=LanguageMenuSender(
                    message_sender=self.message_sender,
                    phrase_repo=self.phrase_repo,
                    language_repo=self.language_repo,
                    select_language_handler_prefix=select_language_handler.prefix,
                ),
                user_repo=self.user_repo,
            )
        return self._show_language_menu_handler

    def get_show_language_menu_handler(self) -> ShowLanguageMenuHandler:
        return self._get_show_language_menu_handler()

    def register_handlers(
        self,
        callback_registry: ICallbackHandlerRegistry,
    ) -> None:
        callback_registry.register(self._get_show_language_menu_handler())
        callback_registry.register(self._get_select_language_handler())
