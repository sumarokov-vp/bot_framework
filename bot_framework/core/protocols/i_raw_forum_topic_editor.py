from typing import Any, Protocol


class IRawForumTopicEditor(Protocol):
    def edit_forum_topic(
        self,
        chat_id: int,
        message_thread_id: int,
        name: str | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> Any: ...
