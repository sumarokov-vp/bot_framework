from typing import Protocol

from bot_framework.flows.request_role_flow.entities import RequestRoleFlowState


class IRequestRoleFlowStateStorage(Protocol):
    def save_selected_role(self, telegram_id: int, role_id: int) -> None: ...

    def get_state(self, telegram_id: int) -> RequestRoleFlowState | None: ...

    def clear_state(self, telegram_id: int) -> None: ...
