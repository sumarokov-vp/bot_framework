from __future__ import annotations

from typing import Any, Protocol


class IMiddleware(Protocol):
    """Abstract middleware protocol for message processing.

    Each messenger integration should implement this protocol
    with platform-specific message and data types.
    """

    def pre_process(
        self,
        message: Any,
        data: dict[str, object],
    ) -> None: ...

    def post_process(
        self,
        message: Any,
        data: dict[str, object],
        exception: Exception | None,
    ) -> None: ...
