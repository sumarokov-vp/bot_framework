from typing import Protocol, TypeVar

TState = TypeVar("TState")


class IStepStateStorage(Protocol[TState]):
    def get(self, user_id: int) -> TState | None: ...

    def save(self, state: TState) -> None: ...

    def delete(self, user_id: int) -> None: ...
