from typing import Protocol


class ISupportTopicManager(Protocol):
    def ensure_topic(self, user_id: int) -> int: ...

    def update_topic_name(self, user_id: int) -> None: ...
