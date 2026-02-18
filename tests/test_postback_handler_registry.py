from __future__ import annotations

from unittest.mock import MagicMock

from bot_framework.platform.facebook.entities.webhook_event import (
    QuickReply,
    WebhookEvent,
    WebhookMessage,
    WebhookPostback,
    WebhookSender,
)
from bot_framework.platform.facebook.services.postback_handler_registry import (
    PostbackHandlerRegistry,
)


def _make_handler(prefix: str):  # noqa: ANN202
    handler = MagicMock()
    handler.prefix = prefix
    handler.allowed_roles = None
    return handler


def _make_postback_event(payload: str):  # noqa: ANN202
    return WebhookEvent(
        sender=WebhookSender(id="12345"),
        recipient=WebhookSender(id="99999"),
        timestamp=1000000,
        postback=WebhookPostback(title="Test", payload=payload),
    )


def _make_quick_reply_event(payload: str):  # noqa: ANN202
    return WebhookEvent(
        sender=WebhookSender(id="12345"),
        recipient=WebhookSender(id="99999"),
        timestamp=1000000,
        message=WebhookMessage(mid="mid.abc", quick_reply=QuickReply(payload=payload)),
    )


def test_register_and_handle_postback():
    registry = PostbackHandlerRegistry()
    handler = _make_handler("menu:")
    registry.register(handler)

    event = _make_postback_event("menu:main")
    registry.handle_event(event)

    handler.handle.assert_called_once()
    callback = handler.handle.call_args[0][0]
    assert callback.data == "menu:main"
    assert callback.user_id == 12345


def test_handle_quick_reply():
    registry = PostbackHandlerRegistry()
    handler = _make_handler("action:")
    registry.register(handler)

    event = _make_quick_reply_event("action:confirm")
    registry.handle_event(event)

    handler.handle.assert_called_once()
    callback = handler.handle.call_args[0][0]
    assert callback.data == "action:confirm"


def test_no_matching_handler():
    registry = PostbackHandlerRegistry()
    handler = _make_handler("menu:")
    registry.register(handler)

    event = _make_postback_event("other:data")
    registry.handle_event(event)

    handler.handle.assert_not_called()


def test_ignores_event_without_payload():
    registry = PostbackHandlerRegistry()
    handler = _make_handler("menu:")
    registry.register(handler)

    event = WebhookEvent(
        sender=WebhookSender(id="12345"),
        recipient=WebhookSender(id="99999"),
        timestamp=1000000,
        message=WebhookMessage(mid="mid.abc", text="hello"),
    )
    registry.handle_event(event)

    handler.handle.assert_not_called()


def test_multiple_handlers_dispatched_by_prefix():
    registry = PostbackHandlerRegistry()
    h1 = _make_handler("menu:")
    h2 = _make_handler("action:")
    registry.register(h1)
    registry.register(h2)

    registry.handle_event(_make_postback_event("action:do"))

    h1.handle.assert_not_called()
    h2.handle.assert_called_once()
