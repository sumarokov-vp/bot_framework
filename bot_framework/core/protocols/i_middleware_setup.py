from typing import Any, Protocol


class IMiddlewareSetup(Protocol):
    def setup_middleware(self, middleware: Any) -> None: ...
