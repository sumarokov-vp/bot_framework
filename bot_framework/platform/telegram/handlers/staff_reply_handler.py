from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from bot_framework.core.entities.bot_message import BotMessage
from bot_framework.core.entities.user import User

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_thread_message_sender import (
        IThreadMessageSender,
    )
    from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import (
        IPhraseRepo,
    )
    from bot_framework.domain.role_management.repos.protocols.i_user_repo import (
        IUserRepo,
    )
    from bot_framework.domain.support_chat.repos.protocols.i_support_topic_repo import (
        ISupportTopicRepo,
    )


class StaffReplyHandler:
    allowed_roles: set[str] | None = None

    def __init__(
        self,
        thread_message_sender: IThreadMessageSender,
        user_repo: IUserRepo,
        phrase_repo: IPhraseRepo,
        support_chat_id: int,
        support_topic_repo: ISupportTopicRepo,
    ) -> None:
        self._thread_message_sender = thread_message_sender
        self._user_repo = user_repo
        self._phrase_repo = phrase_repo
        self._support_chat_id = support_chat_id
        self._support_topic_repo = support_topic_repo
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

        support_topic = self._support_topic_repo.find_by_chat_and_topic(
            chat_id=self._support_chat_id,
            topic_id=thread_id,
        )
        if not support_topic:
            self._logger.warning("No support topic found for topic_id=%s", thread_id)
            return

        user = self._user_repo.find_by_id(support_topic.user_id)
        if not user:
            self._logger.warning("No user found for user_id=%s", support_topic.user_id)
            return

        self._send_to_user(user, text)

    def _send_to_user(self, user: User, text: str) -> None:
        try:
            prefix = self._phrase_repo.get_phrase(
                key="support.staff_prefix",
                language_code=user.language_code,
            )
            self._thread_message_sender.send_message(
                chat_id=user.id,
                text=f"{prefix}\n\n{text}",
            )
        except Exception as er:
            self._logger.error("Failed to send staff reply to user", exc_info=er)
