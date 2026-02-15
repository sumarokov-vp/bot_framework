from uuid import uuid4

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.features.flows.request_role_flow.protocols import IRoleListPresenter
from bot_framework.core.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class ShowRolesHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        role_list_presenter: IRoleListPresenter,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.role_list_presenter = role_list_presenter
        self.user_repo = user_repo
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        user = self.user_repo.get_by_id(id=callback.user_id)
        self.role_list_presenter.present(user)
