from __future__ import annotations

from typing import Any

from bot_framework.core.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.core.protocols.i_message_handler import IMessageHandler


class MaxNextStepHandlerRegistrar:
    def __init__(self) -> None:
        self._handlers: dict[int, IMessageHandler] = {}

    def register(
        self,
        message: BotMessage,
        handler: IMessageHandler,
    ) -> None:
        self._handlers[message.user_id] = handler

    def pop(self, user_id: int) -> IMessageHandler | None:
        return self._handlers.pop(user_id, None)

    def to_bot_message(
        self,
        update: dict[str, Any],
        mid_to_int: dict[str, int],
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

        text = body.get("text")

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
