from typing import Protocol


class ICallbackAnswerer(Protocol):
    def answer(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> None: ...
