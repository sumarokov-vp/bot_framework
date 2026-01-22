from uuid import uuid4

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.flows.request_role_flow.protocols import IRoleListPresenter
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer


class ShowRolesHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        role_list_presenter: IRoleListPresenter,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.role_list_presenter = role_list_presenter
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.message_chat_id:
            raise ValueError("callback.message_chat_id is required but was None")

        language_code = callback.user_language_code or "en"
        self.role_list_presenter.present(
            chat_id=callback.message_chat_id,
            user_id=callback.user_id,
            language_code=language_code,
        )
