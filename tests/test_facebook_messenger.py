from __future__ import annotations

from unittest.mock import MagicMock, patch

from bot_framework.core.entities.button import Button
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.platform.facebook.services.facebook_messenger import (
    MAX_BUTTON_TITLE_LENGTH,
    MAX_QUICK_REPLY_BUTTONS,
    FacebookMessenger,
)


def _make_core(send_result: dict | None = None):  # noqa: ANN202
    core = MagicMock()
    core.api_client.send_message.return_value = send_result or {"message_id": "mid.123"}
    core.flow_message_storage = None
    return core


def test_send_plain_text():
    core = _make_core()
    messenger = FacebookMessenger(core)

    result = messenger.send(chat_id=100, text="Hello")

    core.api_client.send_message.assert_called_once()
    args = core.api_client.send_message.call_args
    assert args[0][0] == "100"
    assert args[0][1] == {"text": "Hello"}
    assert result.chat_id == 100
    assert result.text == "Hello"


def test_send_with_few_buttons_uses_button_template():
    core = _make_core()
    messenger = FacebookMessenger(core)
    keyboard = Keyboard(rows=[[
        Button(text="A", callback_data="a"),
        Button(text="B", callback_data="b"),
    ]])

    messenger.send(chat_id=100, text="Choose", keyboard=keyboard)

    payload = core.api_client.send_message.call_args[0][1]
    assert "attachment" in payload
    template = payload["attachment"]["payload"]
    assert template["template_type"] == "button"
    assert len(template["buttons"]) == 2


def test_send_with_many_buttons_uses_quick_replies():
    core = _make_core()
    messenger = FacebookMessenger(core)
    buttons = [Button(text=f"B{i}", callback_data=f"b{i}") for i in range(5)]
    keyboard = Keyboard(rows=[buttons])

    messenger.send(chat_id=100, text="Choose", keyboard=keyboard)

    payload = core.api_client.send_message.call_args[0][1]
    assert "quick_replies" in payload
    assert len(payload["quick_replies"]) == 5


def test_button_title_truncated():
    core = _make_core()
    messenger = FacebookMessenger(core)
    long_title = "A" * 30
    keyboard = Keyboard(rows=[[Button(text=long_title, callback_data="x")]])

    messenger.send(chat_id=100, text="Hi", keyboard=keyboard)

    payload = core.api_client.send_message.call_args[0][1]
    button = payload["attachment"]["payload"]["buttons"][0]
    assert len(button["title"]) == MAX_BUTTON_TITLE_LENGTH


def test_quick_replies_truncated_to_max():
    core = _make_core()
    messenger = FacebookMessenger(core)
    buttons = [Button(text=f"B{i}", callback_data=f"b{i}") for i in range(20)]
    keyboard = Keyboard(rows=[buttons])

    with patch.object(messenger, "_logger") as mock_logger:
        messenger.send(chat_id=100, text="Pick", keyboard=keyboard)
        mock_logger.warning.assert_called_once()

    payload = core.api_client.send_message.call_args[0][1]
    assert len(payload["quick_replies"]) == MAX_QUICK_REPLY_BUTTONS


def test_send_markdown_as_html_sends_plain():
    core = _make_core()
    messenger = FacebookMessenger(core)

    messenger.send_markdown_as_html(chat_id=100, text="**bold**")

    payload = core.api_client.send_message.call_args[0][1]
    assert payload == {"text": "**bold**"}


def test_send_registers_message_in_flow_storage():
    core = _make_core()
    core.flow_message_storage = MagicMock()
    messenger = FacebookMessenger(core)

    messenger.send(chat_id=100, text="Hi", flow_name="my_flow")

    core.register_message.assert_called_once()
