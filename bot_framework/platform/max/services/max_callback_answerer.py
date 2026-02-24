from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .max_message_core import MaxMessageCore

logger = getLogger(__name__)


class MaxCallbackAnswerer:
    def __init__(self, core: MaxMessageCore) -> None:
        self._core = core

    def answer(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> None:
        body: dict[str, object] = {}
        if text:
            body["notification"] = text
        self._core.api_client.answer_callback(callback_query_id, body)
        logger.debug("Answered callback %s", callback_query_id)
