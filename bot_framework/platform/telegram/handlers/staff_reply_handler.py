from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from bot_framework.core.entities.bot_message import BotMessage

if TYPE_CHECKING:
    from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo
    from telebot import TeleBot


class StaffReplyHandler:
    allowed_roles: set[str] | None = None

    def __init__(
        self,
        bot: TeleBot,
        user_repo: IUserRepo,
        support_chat_id: int,
    ) -> None:
        self._bot = bot
        self._user_repo = user_repo
        self._support_chat_id = support_chat_id
        self._logger = getLogger(__name__)

    def handle(self, message: BotMessage) -> None:
        original = message.get_original()
        if not original:
            return

        from_user = original.from_user
        if not from_user or from_user.is_bot:
            return

        thread_id = original.message_thread_id
        if not thread_id:
            return

        text = original.text
        if not text:
            return

        user = self._find_user_by_topic(thread_id)
        if not user:
            self._logger.warning("No user found for topic_id=%s", thread_id)
            return

        self._send_to_user(user.id, text)

    def _find_user_by_topic(self, topic_id: int):  # noqa: ANN202
        return self._user_repo.find_by_support_topic_id(topic_id)

    def _send_to_user(self, chat_id: int, text: str) -> None:
        try:
            self._bot.send_message(
                chat_id=chat_id,
                text=f"👤 Сотрудник:\n\n{text}",
            )
        except Exception as er:
            self._logger.error("Failed to send staff reply to user", exc_info=er)
