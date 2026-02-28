from __future__ import annotations

from logging import getLogger
from typing import Any

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.keyboard import Keyboard
from bot_framework.core.entities.parse_mode import ParseMode

from .max_core_protocols import IMaxMessengerCore
from .max_keyboard_validator import MaxKeyboardValidator

logger = getLogger(__name__)


class MaxMessenger:
    def __init__(self, core: IMaxMessengerCore, keyboard_validator: MaxKeyboardValidator) -> None:
        self._core = core
        self._keyboard_validator = keyboard_validator
        self._logger = getLogger(__name__)

    def send(
        self,
        chat_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        resolved_chat_id = self._core.dialog_repo.get_chat_id(chat_id) or chat_id
        body = self._build_message_body(text, parse_mode, keyboard)
        result = self._core.api_client.send_message(body, chat_id=resolved_chat_id)
        message_data = result.get("message", {})
        bot_message = self._core.create_bot_message(chat_id, message_data)
        self._core.register_message(chat_id, bot_message.message_id, flow_name)
        return bot_message

    def send_markdown_as_html(
        self,
        chat_id: int,
        text: str,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        return self.send(chat_id, text, ParseMode.MARKDOWN, keyboard, flow_name)

    def replace(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        keyboard: Keyboard | None = None,
        flow_name: str | None = None,
    ) -> BotMessage:
        mid = self._core.int_to_mid(message_id)
        body = self._build_message_body(text, parse_mode, keyboard)
        if "attachments" not in body:
            body["attachments"] = []
        self._core.api_client.edit_message(mid, body)
        self._core.register_message(chat_id, message_id, flow_name)
        return BotMessage(chat_id=chat_id, message_id=message_id, text=text)

    def send_media_group(
        self,
        chat_id: int,
        photo_urls: list[str],
        caption: str | None = None,
    ) -> None:
        if not photo_urls:
            return
        resolved_chat_id = self._core.dialog_repo.get_chat_id(chat_id) or chat_id
        for i, url in enumerate(photo_urls[:10]):
            body: dict[str, Any] = {
                "attachments": [{"type": "image", "payload": {"url": url}}],
            }
            if caption and i == 0:
                body["text"] = caption
                body["format"] = "html"
            self._core.api_client.send_message(body, chat_id=resolved_chat_id)

    def delete(self, chat_id: int, message_id: int) -> None:
        mid = self._core.int_to_mid(message_id)
        self._core.api_client.delete_message(mid)
        self._logger.debug("Deleted message mid=%s chat_id=%s", mid, chat_id)

    def send_document(
        self,
        chat_id: int,
        document: bytes,
        filename: str,
        keyboard: Keyboard | None = None,
    ) -> BotMessage:
        upload_endpoint = self._core.api_client.get_upload_url("file")
        upload_url = upload_endpoint["url"]
        upload_token = upload_endpoint.get("token", "")

        self._core.api_client.upload_file(upload_url, document, filename)

        attachments: list[dict[str, Any]] = [
            {
                "type": "file",
                "payload": {"token": upload_token},
            }
        ]
        body: dict[str, Any] = {"attachments": attachments}
        if keyboard:
            attachments.append(self._core.convert_keyboard(keyboard))

        resolved_chat_id = self._core.dialog_repo.get_chat_id(chat_id) or chat_id
        result = self._core.api_client.send_message(body, chat_id=resolved_chat_id)
        message_data = result.get("message", {})
        bot_message = self._core.create_bot_message(resolved_chat_id, message_data)
        return bot_message

    def download_document(self, file_id: str) -> bytes:
        return self._core.api_client.download_file(file_id)

    def _build_message_body(
        self,
        text: str,
        parse_mode: ParseMode,
        keyboard: Keyboard | None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"text": text}

        if parse_mode == ParseMode.HTML:
            body["format"] = "html"
        elif parse_mode == ParseMode.MARKDOWN:
            body["format"] = "markdown"

        if keyboard:
            self._keyboard_validator.validate(keyboard)
            body["attachments"] = [self._core.convert_keyboard(keyboard)]

        return body
