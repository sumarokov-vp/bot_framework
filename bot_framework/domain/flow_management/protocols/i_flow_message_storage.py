from typing import Protocol, runtime_checkable


@runtime_checkable
class IFlowMessageStorage(Protocol):
    def add_message(
        self, telegram_id: int, flow_name: str, message_id: int
    ) -> None: ...

    def get_messages(self, telegram_id: int, flow_name: str) -> list[int]: ...

    def clear_messages(self, telegram_id: int, flow_name: str) -> None: ...

    def clear_all_messages(self, telegram_id: int) -> None: ...
