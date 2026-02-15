from typing import Protocol, runtime_checkable


@runtime_checkable
class IFlowStackValidator(Protocol):
    def validate_push(self, user_id: int, flow_name: str) -> None: ...
