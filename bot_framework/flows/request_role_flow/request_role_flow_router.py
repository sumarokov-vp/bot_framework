from bot_framework.entities.bot_message import BotMessageUser
from bot_framework.flows.request_role_flow.protocols import IRoleListPresenter


class RequestRoleFlowRouter:
    def __init__(
        self,
        role_list_presenter: IRoleListPresenter,
    ) -> None:
        self.role_list_presenter = role_list_presenter

    def start(self, user: BotMessageUser, chat_id: int) -> None:
        language_code = user.language_code or "en"
        self.role_list_presenter.present(
            chat_id=chat_id,
            user_id=user.id,
            language_code=language_code,
        )
