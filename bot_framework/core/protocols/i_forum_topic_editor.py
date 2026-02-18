from typing import Protocol


class IForumTopicEditor(Protocol):
    def edit_topic(self, chat_id: int, topic_id: int, name: str) -> None: ...
