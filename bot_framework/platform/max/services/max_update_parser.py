from __future__ import annotations

from dataclasses import dataclass
from typing import Any

BOT_STARTED_COMMAND = "/start"


@dataclass
class MaxParsedUpdate:
    update_type: str
    sender: dict[str, Any]
    recipient: dict[str, Any]
    text: str | None
    mid: str
    command: str | None
    raw_update: dict[str, Any]


class MaxUpdateParser:
    def parse(self, update: dict[str, Any]) -> MaxParsedUpdate:
        update_type = update.get("update_type", "")

        if update_type == "bot_started":
            return self._parse_bot_started(update)
        if update_type == "message_created":
            return self._parse_message_created(update)
        if update_type == "message_callback":
            return self._parse_message_callback(update)

        return MaxParsedUpdate(
            update_type=update_type,
            sender={},
            recipient={},
            text=None,
            mid="",
            command=None,
            raw_update=update,
        )

    def _parse_bot_started(self, update: dict[str, Any]) -> MaxParsedUpdate:
        user = update.get("user", {})
        chat_id = update.get("chat_id")
        user_id = user.get("user_id")

        recipient = {
            "chat_id": chat_id,
            "user_id": user_id,
            "chat_type": "dialog",
        }

        return MaxParsedUpdate(
            update_type="bot_started",
            sender=user,
            recipient=recipient,
            text=BOT_STARTED_COMMAND,
            mid="",
            command=BOT_STARTED_COMMAND,
            raw_update=update,
        )

    def _parse_message_created(self, update: dict[str, Any]) -> MaxParsedUpdate:
        message = update.get("message", {})
        body = message.get("body", {}) or message.get("message", {})
        sender = message.get("sender", {})
        recipient = message.get("recipient", {})
        mid = body.get("mid", "")
        text = body.get("text")

        if text and text.startswith("/"):
            command = text.split()[0]
        elif not text and not mid:
            command = BOT_STARTED_COMMAND
        else:
            command = None

        return MaxParsedUpdate(
            update_type="message_created",
            sender=sender,
            recipient=recipient,
            text=text,
            mid=mid,
            command=command,
            raw_update=update,
        )

    def _parse_message_callback(self, update: dict[str, Any]) -> MaxParsedUpdate:
        callback = update.get("callback", {})
        sender = callback.get("user", {})
        message = update.get("message", {})
        body = message.get("body", {}) or message.get("message", {})
        mid = body.get("mid", "")

        return MaxParsedUpdate(
            update_type="message_callback",
            sender=sender,
            recipient={},
            text=None,
            mid=mid,
            command=None,
            raw_update=update,
        )
