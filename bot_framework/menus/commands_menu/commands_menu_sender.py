from bot_framework.entities.button import Button
from bot_framework.entities.keyboard import Keyboard
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.menus.commands_menu.i_commands_menu_sender import ICommandsMenuSender
from bot_framework.menus.start_menu.main_menu_sender import MenuButtonConfig
from bot_framework.protocols.i_message_sender import IMessageSender


class CommandsMenuSender(ICommandsMenuSender):
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        title_phrase_key: str,
        buttons: list[MenuButtonConfig],
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.title_phrase_key = title_phrase_key
        self.buttons = buttons

    def send(self, chat_id: int, language_code: str) -> None:
        text = self.phrase_repo.get_phrase(
            key=self.title_phrase_key,
            language_code=language_code,
        )

        rows = []
        for button_config in self.buttons:
            button = Button(
                text=self.phrase_repo.get_phrase(
                    key=button_config.phrase_key,
                    language_code=language_code,
                ),
                callback_data=button_config.handler.prefix,
            )
            rows.append([button])

        keyboard = Keyboard(rows=rows)

        self.message_sender.send(
            chat_id=chat_id,
            text=text,
            keyboard=keyboard,
        )
