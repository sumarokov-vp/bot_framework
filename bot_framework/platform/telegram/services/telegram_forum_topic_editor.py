from __future__ import annotations

from typing import TYPE_CHECKING

from telebot.apihelper import ApiTelegramException

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_raw_forum_topic_editor import (
        IRawForumTopicEditor,
    )


class TelegramForumTopicEditor:
    def __init__(self, raw_forum_topic_editor: IRawForumTopicEditor) -> None:
        self._raw_forum_topic_editor = raw_forum_topic_editor

    def edit_topic(self, chat_id: int, topic_id: int, name: str) -> None:
        try:
            self._raw_forum_topic_editor.edit_forum_topic(
                chat_id=chat_id,
                message_thread_id=topic_id,
                name=name,
            )
        except ApiTelegramException as exc:
            if "TOPIC_NOT_MODIFIED" in exc.description:
                return
            raise
