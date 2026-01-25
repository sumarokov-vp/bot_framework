from bot_framework.entities.button import Button
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.user import User
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.menus.start_menu.i_main_menu_sender import IMainMenuSender
from bot_framework.protocols.i_callback_handler import ICallbackHandler
from bot_framework.protocols.i_message_sender import IMessageSender


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
        welcome_phrase_key: str,
        buttons: list[MenuButtonConfig] | None = None,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.welcome_phrase_key = welcome_phrase_key
        self.buttons = buttons if buttons is not None else []

    def add_button(self, config: MenuButtonConfig) -> None:
        self.buttons.append(config)

    def send(self, user: User) -> None:
        text = self.phrase_repo.get_phrase(
            key=self.welcome_phrase_key,
            language_code=user.language_code,
        )

        rows = []
        for button_config in self.buttons:
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
