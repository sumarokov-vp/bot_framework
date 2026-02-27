from logging import getLogger

from .max_core_protocols import IMaxCallbackCore

logger = getLogger(__name__)


class MaxCallbackAnswerer:
    def __init__(self, core: IMaxCallbackCore) -> None:
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
