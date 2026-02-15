from uuid import uuid4

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.features.flows.request_role_flow.protocols import IRoleAssigner
from bot_framework.core.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class ApproveRoleHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        user_repo: IUserRepo,
        role_assigner: IRoleAssigner,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.user_repo = user_repo
        self.role_assigner = role_assigner
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.data:
            raise ValueError("callback.data is required but was None")

        parts = callback.data.split(":")
        if len(parts) < 3:
            raise ValueError(f"Invalid callback data format: {callback.data}")

        role_id = int(parts[1])
        user_id = int(parts[2])

        user = self.user_repo.find_by_id(id=user_id)
        if not user:
            return

        self.role_assigner.assign_and_notify(user, role_id)
