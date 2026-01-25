from bot_framework.entities.button import Button
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.user import User
from bot_framework.language_management.repos.protocols.i_language_repo import (
    ILanguageRepo,
)
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.menus.language_menu.i_language_menu_sender import ILanguageMenuSender
from bot_framework.protocols.i_message_sender import IMessageSender


class LanguageMenuSender(ILanguageMenuSender):
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        language_repo: ILanguageRepo,
        select_language_handler_prefix: str,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.language_repo = language_repo
        self.select_language_handler_prefix = select_language_handler_prefix

    def send(self, user: User) -> None:
        text = self.phrase_repo.get_phrase(
            key="language.select_title",
            language_code=user.language_code,
        )

        languages = self.language_repo.get_all()
        rows = []
        for lang in languages:
            is_current = lang.code == user.language_code
            button_text = f"\u2713 {lang.native_name}" if is_current else lang.native_name
            rows.append(
                [
                    Button(
                        text=button_text,
                        callback_data=f"{self.select_language_handler_prefix}:{lang.code}",
                    )
                ]
            )

        keyboard = Keyboard(rows=rows)
        self.message_sender.send(chat_id=user.id, text=text, keyboard=keyboard)
