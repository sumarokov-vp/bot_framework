from bot_framework.core.entities.user import User
from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.core.protocols.i_message_sender import IMessageSender


class RoleRejectionNotifier:
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo

    def notify(self, user: User) -> None:
        text = self.phrase_repo.get_phrase(
            key="request_role.rejected",
            language_code=user.language_code,
        )

        self.message_sender.send(chat_id=user.id, text=text)
