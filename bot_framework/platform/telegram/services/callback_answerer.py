from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .telegram_message_core import TelegramMessageCore


class CallbackAnswerer:
    def __init__(self, core: TelegramMessageCore) -> None:
        self._core = core

    def answer(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> None:
        self._core.bot.answer_callback_query(
            callback_query_id, text=text, show_alert=show_alert
        )
