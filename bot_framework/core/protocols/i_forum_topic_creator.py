from typing import Protocol


class IForumTopicCreator(Protocol):
    def create_topic(self, chat_id: int, name: str) -> int: ...
