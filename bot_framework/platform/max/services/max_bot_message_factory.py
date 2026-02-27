from __future__ import annotations

from typing import Any

from bot_framework.core.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.platform.max.services.max_update_parser import MaxParsedUpdate


class MaxBotMessageFactory:
    @staticmethod
    def from_parsed(parsed: MaxParsedUpdate, mid_to_int: dict[str, int]) -> BotMessage:
        user_id = int(parsed.sender.get("user_id", 0))
        chat_id_raw = parsed.recipient.get("chat_id") or parsed.recipient.get("user_id")
        chat_id = int(chat_id_raw) if chat_id_raw is not None else user_id
        raw_mid = parsed.mid
        message_id = mid_to_int.get(raw_mid, hash(raw_mid) & 0x7FFFFFFF)
        text = parsed.command or parsed.text
        from_user = BotMessageUser(id=user_id)
        bot_message = BotMessage(
            chat_id=chat_id,
            message_id=message_id,
            user_id=user_id,
            text=text,
            from_user=from_user,
        )
        bot_message.set_original(parsed.raw_update)
        return bot_message

    @staticmethod
    def from_update(
        update: dict[str, Any],
        mid_to_int: dict[str, int],
        command_override: str | None = None,
    ) -> BotMessage:
        message = update.get("message", {})
        sender = message.get("sender", {})
        recipient = message.get("recipient", {})
        body = message.get("body", {}) or message.get("message", {})

        user_id = int(sender.get("user_id", 0))
        chat_id_raw = recipient.get("chat_id") or recipient.get("user_id")
        chat_id = int(chat_id_raw) if chat_id_raw is not None else user_id

        raw_mid = body.get("mid", "")
        message_id = mid_to_int.get(raw_mid, hash(raw_mid) & 0x7FFFFFFF)

        text = command_override or body.get("text")

        from_user = BotMessageUser(id=user_id)
        bot_message = BotMessage(
            chat_id=chat_id,
            message_id=message_id,
            user_id=user_id,
            text=text,
            from_user=from_user,
        )
        bot_message.set_original(update)
        return bot_message
