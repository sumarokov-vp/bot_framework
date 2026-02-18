from __future__ import annotations

from logging import getLogger

from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.core.protocols.i_callback_handler import ICallbackHandler
from bot_framework.platform.facebook.entities.webhook_event import WebhookEvent


class PostbackHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, ICallbackHandler] = {}
        self._logger = getLogger(__name__)

    def register(self, handler: ICallbackHandler) -> None:
        self._handlers[handler.prefix] = handler

    def handle_event(self, event: WebhookEvent) -> None:
        payload = self._extract_payload(event)
        if payload is None:
            return

        handler = self._find_handler(payload)
        if handler is None:
            self._logger.warning("No handler for payload: %s", payload)
            return

        bot_callback = BotCallback(
            id=event.message.mid if event.message else str(event.timestamp),
            user_id=int(event.sender.id),
            data=payload,
            message_id=hash(event.message.mid) if event.message else None,
            message_chat_id=int(event.sender.id),
        )
        bot_callback.set_original(event)
        handler.handle(bot_callback)

    def _extract_payload(self, event: WebhookEvent) -> str | None:
        if event.postback:
            return event.postback.payload
        if event.message and event.message.quick_reply:
            return event.message.quick_reply.payload
        return None

    def _find_handler(self, payload: str) -> ICallbackHandler | None:
        for prefix, handler in self._handlers.items():
            if payload.startswith(prefix):
                return handler
        return None
