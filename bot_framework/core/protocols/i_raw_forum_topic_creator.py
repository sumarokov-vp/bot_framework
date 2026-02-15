from typing import Any, Protocol


class IRawForumTopicCreator(Protocol):
    def create_forum_topic(
        self,
        chat_id: int,
        name: str,
        icon_color: int | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> Any: ...
