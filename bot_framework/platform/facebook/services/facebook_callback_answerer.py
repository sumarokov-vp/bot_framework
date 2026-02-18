from __future__ import annotations


class FacebookCallbackAnswerer:
    def answer(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> None:
        pass
