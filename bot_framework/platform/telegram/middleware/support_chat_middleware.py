from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from telebot.types import Message

from bot_framework.platform.telegram.middleware.telegram_base_middleware import (
    TelegramBaseMiddleware,
)

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_support_topic_manager import ISupportTopicManager


class SupportChatMiddleware(TelegramBaseMiddleware):
    update_types = ["message"]

    def __init__(
        self,
        support_chat_id: int,
        support_topic_manager: ISupportTopicManager,
        bot: object,
    ) -> None:
        super().__init__()
        self._support_chat_id = support_chat_id
        self._support_topic_manager = support_topic_manager
        self._bot = bot
        self._logger = getLogger(__name__)
        self.update_sensitive = False

    def pre_process(
        self,
        message: Message,
        data: dict[str, object],
    ) -> None:
        if message.chat.id == self._support_chat_id:
            return

        from_user = message.from_user
        if not from_user:
            return

        full_name = self._build_full_name(
            first_name=from_user.first_name,
            last_name=from_user.last_name,
        )

        topic_id = self._support_topic_manager.ensure_topic(
            user_id=from_user.id,
            full_name=full_name,
        )

        self._forward_to_support(message, topic_id)

    def _build_full_name(
        self,
        first_name: str | None,
        last_name: str | None,
    ) -> str:
        parts = [p for p in (first_name, last_name) if p]
        return " ".join(parts) or "Unknown"

    def _forward_to_support(self, message: Message, topic_id: int) -> None:
        from telebot import TeleBot

        bot: TeleBot = self._bot  # type: ignore[assignment]
        try:
            bot.forward_message(
                chat_id=self._support_chat_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                message_thread_id=topic_id,
            )
        except Exception as er:
            self._logger.error("Failed to forward message to support chat", exc_info=er)

    def post_process(
        self,
        message: Message,
        data: dict[str, object],
        exception: Exception | None,
    ) -> None:
        pass
