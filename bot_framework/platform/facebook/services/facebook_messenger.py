from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.parse_mode import ParseMode

if TYPE_CHECKING:
    from .facebook_message_core import FacebookMessageCore

MAX_BUTTON_TEMPLATE_BUTTONS = 3
MAX_QUICK_REPLY_BUTTONS = 13
MAX_BUTTON_TITLE_LENGTH = 20


class FacebookMessenger:
    def __init__(self, core: FacebookMessageCore) -> None:
        self._core = core
        self._logger = getLogger(__name__)

    def send(
        self,
        chat_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        recipient_id = str(chat_id)
        payload = self._build_message_payload(text, keyboard)
        result = self._core.api_client.send_message(recipient_id, payload)
        message_id = result.get("message_id", "")
        self._core.register_message(chat_id, hash(message_id), flow_name)
        return BotMessage(
            chat_id=chat_id,
            message_id=hash(message_id),
            text=text,
        )

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        return self.send(chat_id, text, ParseMode.PLAIN, keyboard, flow_name)

    def send_media_group(
        self,
        chat_id: int,
        photo_urls: list[str],
        caption: str | None = None,
    ) -> None:
        if not photo_urls:
            return
        recipient_id = str(chat_id)
        for i, url in enumerate(photo_urls[:10]):
            payload: dict[str, Any] = {
                "attachment": {
                    "type": "image",
                    "payload": {"url": url},
                },
            }
            if caption and i == 0:
                payload["text"] = caption
            self._core.api_client.send_message(recipient_id, payload)

    def delete(self, chat_id: int, message_id: int) -> None:
        self._logger.debug("Facebook message deletion is limited; message_id=%s", message_id)

    def _build_message_payload(self, text: str, keyboard: Keyboard | None) -> dict[str, Any]:
        if not keyboard:
            return {"text": text}

        buttons = self._flatten_keyboard(keyboard)

        if len(buttons) <= MAX_BUTTON_TEMPLATE_BUTTONS:
            return self._build_button_template(text, buttons)

        return self._build_quick_replies(text, buttons)

    def _flatten_keyboard(self, keyboard: Keyboard) -> list[dict[str, str]]:
        buttons: list[dict[str, str]] = []
        for row in keyboard.rows:
            for button in row:
                buttons.append({
                    "title": button.text[:MAX_BUTTON_TITLE_LENGTH],
                    "payload": button.callback_data,
                })
        return buttons

    def _build_button_template(
        self, text: str, buttons: list[dict[str, str]]
    ) -> dict[str, Any]:
        return {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": [
                        {
                            "type": "postback",
                            "title": b["title"],
                            "payload": b["payload"],
                        }
                        for b in buttons[:MAX_BUTTON_TEMPLATE_BUTTONS]
                    ],
                },
            }
        }

    def _build_quick_replies(
        self, text: str, buttons: list[dict[str, str]]
    ) -> dict[str, Any]:
        if len(buttons) > MAX_QUICK_REPLY_BUTTONS:
            self._logger.warning(
                "Facebook supports max %d quick replies, truncating from %d",
                MAX_QUICK_REPLY_BUTTONS,
                len(buttons),
            )

        return {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": b["title"],
                    "payload": b["payload"],
                }
                for b in buttons[:MAX_QUICK_REPLY_BUTTONS]
            ],
        }
