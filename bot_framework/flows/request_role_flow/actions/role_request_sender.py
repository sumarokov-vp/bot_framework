from bot_framework.entities.button import Button
from bot_framework.entities.keyboard import Keyboard
from bot_framework.entities.role import Role
from bot_framework.entities.user import User
from bot_framework.flows.request_role_flow.exceptions import NoSupervisorsFoundError
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class RoleRequestSender:
    def __init__(
        self,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        user_repo: IUserRepo,
        approve_handler_prefix: str,
        reject_handler_prefix: str,
    ) -> None:
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.user_repo = user_repo
        self.approve_handler_prefix = approve_handler_prefix
        self.reject_handler_prefix = reject_handler_prefix

    def send_to_supervisors(
        self,
        requester: User,
        role: Role,
    ) -> None:
        supervisors = self.user_repo.get_by_role_name(role_name="supervisors")
        if not supervisors:
            raise NoSupervisorsFoundError()

        for supervisor in supervisors:
            language_code = supervisor.language_code

            title = self.phrase_repo.get_phrase(
                key="request_role.supervisor.title",
                language_code=language_code,
            )

            requester_name = requester.username or requester.first_name or str(requester.id)
            text = f"{title}\n\nUser: {requester_name}\nRole: {role.name}"

            approve_text = self.phrase_repo.get_phrase(
                key="request_role.button.approve",
                language_code=language_code,
            )
            reject_text = self.phrase_repo.get_phrase(
                key="request_role.button.reject",
                language_code=language_code,
            )

            keyboard = Keyboard(
                rows=[
                    [
                        Button(
                            text=approve_text,
                            callback_data=f"{self.approve_handler_prefix}:{role.id}:{requester.id}",
                        ),
                        Button(
                            text=reject_text,
                            callback_data=f"{self.reject_handler_prefix}:{role.id}:{requester.id}",
                        ),
                    ]
                ]
            )

            self.message_sender.send(
                chat_id=supervisor.id,
                text=text,
                keyboard=keyboard,
            )
