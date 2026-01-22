from collections.abc import Sequence
from typing import (
    Protocol,
    TypeVar,
)

T = TypeVar("T", covariant=True)


class ReadSequenceByUserIdProtocol(Protocol[T]):
    def get_by_user_id(self, user_id: int) -> Sequence[T]: ...
