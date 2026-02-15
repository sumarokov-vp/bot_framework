from typing import Protocol, runtime_checkable


@runtime_checkable
class IFlowMessageDeleter(Protocol):
    def delete_flow_messages(self, chat_id: int, flow_name: str) -> None: ...

    def delete_all_flow_messages(self, chat_id: int) -> None: ...
