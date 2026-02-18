from __future__ import annotations

from typing import TYPE_CHECKING

from bot_framework.core.entities.support_topic import SupportTopic
from bot_framework.core.entities.user import User

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_forum_topic_creator import IForumTopicCreator
    from bot_framework.core.protocols.i_forum_topic_editor import IForumTopicEditor
    from bot_framework.domain.role_management.repos.protocols.i_user_repo import (
        IUserRepo,
    )
    from bot_framework.domain.support_chat.repos.protocols.i_support_topic_repo import (
        ISupportTopicRepo,
    )


MAX_TOPIC_NAME_LENGTH = 128

DEFAULT_TOPIC_NAME_FORMAT = "{bot_name} | {full_name} 📞{phone} @{username}"


class SupportTopicManager:
    def __init__(
        self,
        support_chat_id: int,
        user_repo: IUserRepo,
        forum_topic_creator: IForumTopicCreator,
        forum_topic_editor: IForumTopicEditor,
        support_topic_repo: ISupportTopicRepo,
        bot_name: str,
        topic_name_format: str = DEFAULT_TOPIC_NAME_FORMAT,
    ) -> None:
        self._support_chat_id = support_chat_id
        self._user_repo = user_repo
        self._forum_topic_creator = forum_topic_creator
        self._forum_topic_editor = forum_topic_editor
        self._support_topic_repo = support_topic_repo
        self._bot_name = bot_name
        self._topic_name_format = topic_name_format

    def ensure_topic(self, user_id: int) -> int:
        existing = self._support_topic_repo.find_by_user_and_chat(
            user_id=user_id,
            chat_id=self._support_chat_id,
        )
        if existing:
            return existing.topic_id

        user = self._user_repo.get_by_id(user_id)
        topic_name = self._build_topic_name(user)
        topic_id = self._forum_topic_creator.create_topic(
            chat_id=self._support_chat_id,
            name=topic_name,
        )

        self._support_topic_repo.create(
            SupportTopic(
                user_id=user_id,
                chat_id=self._support_chat_id,
                topic_id=topic_id,
            )
        )
        return topic_id

    def update_topic_name(self, user_id: int) -> None:
        existing = self._support_topic_repo.find_by_user_and_chat(
            user_id=user_id,
            chat_id=self._support_chat_id,
        )
        if not existing:
            return

        user = self._user_repo.get_by_id(user_id)
        topic_name = self._build_topic_name(user)
        self._forum_topic_editor.edit_topic(
            chat_id=self._support_chat_id,
            topic_id=existing.topic_id,
            name=topic_name,
        )

    def _build_topic_name(self, user: User) -> str:
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip() or "Unknown"
        username = user.username or "unknown"
        phone = user.phone_number or "unknown"

        name = self._topic_name_format.format(
            bot_name=self._bot_name,
            full_name=full_name,
            phone=phone,
            username=username,
        )
        return name[:MAX_TOPIC_NAME_LENGTH]
