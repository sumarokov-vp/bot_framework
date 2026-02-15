from uuid import uuid4

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.features.flows.request_role_flow.exceptions import (
    NoSupervisorsFoundError,
)
from bot_framework.features.flows.request_role_flow.protocols import (
    IRequestRoleFlowStateStorage,
    IRoleRequestSender,
)
from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import (
    IPhraseRepo,
)
from bot_framework.core.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.core.protocols.i_message_sender import IMessageSender
from bot_framework.domain.role_management.repos.protocols.i_role_repo import IRoleRepo
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class RoleSelectionHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        role_repo: IRoleRepo,
        user_repo: IUserRepo,
        state_storage: IRequestRoleFlowStateStorage,
        role_request_sender: IRoleRequestSender,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.role_repo = role_repo
        self.user_repo = user_repo
        self.state_storage = state_storage
        self.role_request_sender = role_request_sender
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.data:
            raise ValueError("callback.data is required but was None")

        parts = callback.data.split(":")
        if len(parts) < 2:
            raise ValueError(f"Invalid callback data format: {callback.data}")

        role_id = int(parts[1])

        requester = self.user_repo.get_by_id(id=callback.user_id)

        self.state_storage.save_selected_role(telegram_id=requester.id, role_id=role_id)

        role = self.role_repo.get_by_id(id=role_id)

        user_roles = self.role_repo.get_user_roles(user_id=requester.id)
        if any(r.id == role_id for r in user_roles):
            phrase_key = "request_role.already_has_role"
        else:
            try:
                self.role_request_sender.send_to_supervisors(
                    requester=requester, role=role
                )
                phrase_key = "request_role.sent"
            except NoSupervisorsFoundError:
                phrase_key = "request_role.no_supervisors"

        text = self.phrase_repo.get_phrase(
            key=phrase_key,
            language_code=requester.language_code,
        )
        self.message_sender.send(chat_id=requester.id, text=text)

        self.state_storage.clear_state(telegram_id=requester.id)
