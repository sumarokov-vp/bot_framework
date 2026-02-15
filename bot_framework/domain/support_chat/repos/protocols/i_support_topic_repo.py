from typing import Protocol

from bot_framework.core.entities.support_topic import SupportTopic


class ISupportTopicRepo(Protocol):
    def find_by_user_and_chat(
        self,
        user_id: int,
        chat_id: int,
    ) -> SupportTopic | None: ...

    def create(self, entity: SupportTopic) -> SupportTopic: ...

    def find_by_chat_and_topic(
        self,
        chat_id: int,
        topic_id: int,
    ) -> SupportTopic | None: ...

    def delete_by_user_and_chat(
        self,
        user_id: int,
        chat_id: int,
    ) -> None: ...
