from typing import Protocol


class ICallbackAnswererBot(Protocol):
    def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> bool: ...
