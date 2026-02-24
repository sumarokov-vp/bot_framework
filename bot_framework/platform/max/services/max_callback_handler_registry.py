from __future__ import annotations

from logging import getLogger
from typing import Any

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.core.protocols.i_callback_handler import ICallbackHandler


class MaxCallbackHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, ICallbackHandler] = {}
        self._logger = getLogger(__name__)

    def register(self, handler: ICallbackHandler) -> None:
        self._handlers[handler.prefix] = handler

    def dispatch(self, update: dict[str, Any], mid_to_int: dict[str, int]) -> None:
        callback = update.get("callback", {})
        payload = callback.get("payload")
        if payload is None:
            return

        handler = self._find_handler(payload)
        if handler is None:
            self._logger.warning("No handler for callback payload: %s", payload)
            return

        callback_id = callback.get("callback_id", "")
        user = callback.get("user", {})
        user_id = int(user.get("user_id", 0))

        message = update.get("message", {})
        body = message.get("body", {})
        raw_mid = body.get("mid")
        message_id = mid_to_int.get(raw_mid) if raw_mid else None

        recipient = message.get("recipient", {})
        chat_id = recipient.get("chat_id") or recipient.get("user_id")
        message_chat_id = int(chat_id) if chat_id is not None else None

        bot_callback = BotCallback(
            id=callback_id,
            user_id=user_id,
            data=payload,
            message_id=message_id,
            message_chat_id=message_chat_id,
        )
        bot_callback.set_original(update)
        handler.handle(bot_callback)

    def _find_handler(self, payload: str) -> ICallbackHandler | None:
        for prefix, handler in self._handlers.items():
            if payload.startswith(prefix):
                return handler
        return None
