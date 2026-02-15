from bot_framework.core.entities.user import User
from bot_framework.features.flows.request_role_flow.protocols import IRoleListPresenter


class RequestRoleFlowRouter:
    def __init__(
        self,
        role_list_presenter: IRoleListPresenter,
    ) -> None:
        self.role_list_presenter = role_list_presenter

    def start(self, user: User) -> None:
        self.role_list_presenter.present(user)
