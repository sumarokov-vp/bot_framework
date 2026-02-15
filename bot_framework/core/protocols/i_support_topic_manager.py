from typing import Protocol


class ISupportTopicManager(Protocol):
    def ensure_topic(self, user_id: int, full_name: str) -> int: ...
