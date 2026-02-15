from bot_framework.core.protocols.i_forum_topic_creator import IForumTopicCreator
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


MAX_TOPIC_NAME_LENGTH = 128


class SupportTopicManager:
    def __init__(
        self,
        support_chat_id: int,
        user_repo: IUserRepo,
        forum_topic_creator: IForumTopicCreator,
    ) -> None:
        self._support_chat_id = support_chat_id
        self._user_repo = user_repo
        self._forum_topic_creator = forum_topic_creator

    def ensure_topic(self, user_id: int, full_name: str) -> int:
        user = self._user_repo.get_by_id(user_id)
        if user.support_topic_id:
            return user.support_topic_id

        topic_name = self._build_topic_name(user_id, full_name)
        topic_id = self._forum_topic_creator.create_topic(
            chat_id=self._support_chat_id,
            name=topic_name,
        )

        user.support_topic_id = topic_id
        self._user_repo.update(user)
        return topic_id

    def _build_topic_name(self, user_id: int, full_name: str) -> str:
        suffix = f" [ID:{user_id}]"
        max_name_length = MAX_TOPIC_NAME_LENGTH - len(suffix)
        truncated_name = full_name[:max_name_length]
        return f"{truncated_name}{suffix}"
