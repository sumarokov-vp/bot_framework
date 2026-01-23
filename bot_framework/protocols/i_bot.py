from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol


class IBot(Protocol):
    def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str | None = None,
        reply_markup: Any = None,
    ) -> Any: ...

    def send_document(
        self,
        chat_id: int,
        document: Any,
    ) -> Any: ...

    def edit_message_text(
        self,
        text: str,
        chat_id: int,
        message_id: int,
        parse_mode: str | None = None,
        reply_markup: Any = None,
    ) -> Any: ...

    def delete_message(self, chat_id: int, message_id: int) -> bool: ...

    def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> bool: ...

    def register_callback_query_handler(
        self,
        callback: Callable[..., Any],
        func: Callable[..., bool] | None = None,
    ) -> None: ...

    def register_message_handler(
        self,
        callback: Callable[..., Any],
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[..., bool] | None = None,
    ) -> None: ...

    def register_next_step_handler(
        self,
        message: Any,
        callback: Callable[..., Any],
    ) -> None: ...

    def setup_middleware(self, middleware: Any) -> None: ...

    def infinity_polling(self) -> None: ...
