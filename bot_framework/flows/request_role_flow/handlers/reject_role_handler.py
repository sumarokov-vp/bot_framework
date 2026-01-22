from uuid import uuid4

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.flows.request_role_flow.protocols import IRoleRejectionNotifier
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.role_management.repos.protocols.i_role_repo import IRoleRepo
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class RejectRoleHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        role_repo: IRoleRepo,
        user_repo: IUserRepo,
        role_rejection_notifier: IRoleRejectionNotifier,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.role_repo = role_repo
        self.user_repo = user_repo
        self.role_rejection_notifier = role_rejection_notifier
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.data:
            raise ValueError("callback.data is required but was None")

        parts = callback.data.split(":")
        if len(parts) < 3:
            raise ValueError(f"Invalid callback data format: {callback.data}")

        user_id = int(parts[2])

        user = self.user_repo.find_by_id(id=user_id)
        if not user:
            return

        language_code = user.language_code

        self.role_rejection_notifier.notify(
            user_id=user_id,
            language_code=language_code,
        )
