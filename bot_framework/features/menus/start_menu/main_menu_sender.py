from bot_framework.core.entities.button import Button
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.user import User
from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import (
    IPhraseRepo,
)
from bot_framework.features.menus.start_menu.i_main_menu_sender import IMainMenuSender
from bot_framework.core.protocols.i_callback_handler import ICallbackHandler
from bot_framework.core.protocols.i_message_sender import IMessageSender
from bot_framework.domain.role_management.repos.protocols.i_role_repo import IRoleRepo


class MenuButtonConfig:
    def __init__(
        self,
        phrase_key: str,
        handler: ICallbackHandler,
    ) -> None:
        self.phrase_key = phrase_key
        self.handler = handler


class MainMenuSender(IMainMenuSender):
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        role_repo: IRoleRepo,
        welcome_phrase_key: str,
        buttons: list[MenuButtonConfig] | None = None,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self._role_repo = role_repo
        self.welcome_phrase_key = welcome_phrase_key
        self.buttons = buttons if buttons is not None else []

    def add_button(self, config: MenuButtonConfig) -> None:
        self.buttons.append(config)

    def _is_button_visible(self, handler: ICallbackHandler, user: User) -> bool:
        allowed_roles = getattr(handler, "allowed_roles", None)
        if not allowed_roles:
            return True
        user_roles = self._role_repo.get_user_roles(user_id=user.id)
        user_role_names = {role.name for role in user_roles}
        return bool(user_role_names & allowed_roles)

    def send(self, user: User) -> None:
        text = self.phrase_repo.get_phrase(
            key=self.welcome_phrase_key,
            language_code=user.language_code,
        )

        rows = []
        for button_config in self.buttons:
            if not self._is_button_visible(button_config.handler, user):
                continue
            button = Button(
                text=self.phrase_repo.get_phrase(
                    key=button_config.phrase_key,
                    language_code=user.language_code,
                ),
                callback_data=button_config.handler.prefix,
            )
            rows.append([button])

        keyboard = Keyboard(rows=rows)

        self.message_sender.send(
            chat_id=user.id,
            text=text,
            keyboard=keyboard,
        )
