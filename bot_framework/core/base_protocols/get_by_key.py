from typing import (
    Protocol,
    TypeVar,
)

T = TypeVar("T", covariant=True)


class GetByKeyProtocol(Protocol[T]):
    def get_by_key(self, key: str) -> T: ...
