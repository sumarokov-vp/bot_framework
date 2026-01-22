from bot_framework.entities.button import Button
from bot_framework.entities.keyboard import Keyboard
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.role_management.repos.protocols.i_role_repo import IRoleRepo


class RoleListPresenter:
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        role_repo: IRoleRepo,
        role_selection_handler_prefix: str,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.role_repo = role_repo
        self.role_selection_handler_prefix = role_selection_handler_prefix

    def present(self, chat_id: int, user_id: int, language_code: str) -> None:
        roles = self.role_repo.get_all()

        if not roles:
            text = self.phrase_repo.get_phrase(
                key="request_role.no_roles",
                language_code=language_code,
            )
            self.message_sender.send(chat_id=chat_id, text=text)
            return

        text = self.phrase_repo.get_phrase(
            key="request_role.select_title",
            language_code=language_code,
        )

        user_roles = self.role_repo.get_user_roles(user_id)
        user_role_ids = {role.id for role in user_roles}

        buttons = []
        for role in roles:
            role_text = f"✓ {role.name}" if role.id in user_role_ids else role.name
            buttons.append(
                [
                    Button(
                        text=role_text,
                        callback_data=f"{self.role_selection_handler_prefix}:{role.id}",
                    )
                ]
            )

        keyboard = Keyboard(rows=buttons)
        self.message_sender.send(chat_id=chat_id, text=text, keyboard=keyboard)
