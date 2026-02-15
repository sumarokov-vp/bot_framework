from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_raw_forum_topic_creator import (
        IRawForumTopicCreator,
    )


class TelegramForumTopicCreator:
    def __init__(self, raw_forum_topic_creator: IRawForumTopicCreator) -> None:
        self._raw_forum_topic_creator = raw_forum_topic_creator

    def create_topic(self, chat_id: int, name: str) -> int:
        result = self._raw_forum_topic_creator.create_forum_topic(
            chat_id=chat_id,
            name=name,
        )
        return result.message_thread_id
