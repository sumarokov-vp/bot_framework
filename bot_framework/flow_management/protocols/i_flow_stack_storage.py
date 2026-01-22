from typing import Protocol, runtime_checkable

from bot_framework.flow_management.entities import FlowStackEntry


@runtime_checkable
class IFlowStackStorage(Protocol):
    def push(self, telegram_id: int, entry: FlowStackEntry) -> None: ...

    def pop(self, telegram_id: int) -> FlowStackEntry | None: ...

    def get_stack(self, telegram_id: int) -> list[FlowStackEntry]: ...

    def clear(self, telegram_id: int) -> None: ...
