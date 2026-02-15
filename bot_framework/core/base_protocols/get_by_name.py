from typing import (
    Protocol,
    TypeVar,
)

T = TypeVar("T")


class GetByNameProtocol(Protocol[T]):
    def get_by_name(self, name: str) -> list[T]: ...
