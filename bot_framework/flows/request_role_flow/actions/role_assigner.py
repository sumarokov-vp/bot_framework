from bot_framework.entities.user import User
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.role_management.repos.protocols.i_role_repo import IRoleRepo


class RoleAssigner:
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        role_repo: IRoleRepo,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.role_repo = role_repo

    def assign_and_notify(self, user: User, role_id: int) -> None:
        self.role_repo.assign_role(user_id=user.id, role_id=role_id)

        text = self.phrase_repo.get_phrase(
            key="request_role.approved",
            language_code=user.language_code,
        )

        self.message_sender.send(chat_id=user.id, text=text)
