from unittest.mock import MagicMock

from bot_framework.core.entities.support_topic import SupportTopic
from bot_framework.core.entities.user import User
from bot_framework.domain.support_chat.services.support_topic_manager import (
    SupportTopicManager,
)


def _make_user(
    id: int = 123,
    first_name: str | None = "John",
    last_name: str | None = "Doe",
    username: str | None = "johndoe",
    phone_number: str | None = "+79991234567",
) -> User:
    return User(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        phone_number=phone_number,
    )


def _make_manager(
    bot_name: str = "TestBot",
    topic_name_format: str | None = None,
    support_chat_id: int = -1001234567890,
) -> tuple[SupportTopicManager, MagicMock, MagicMock, MagicMock, MagicMock]:
    user_repo = MagicMock()
    forum_topic_creator = MagicMock()
    forum_topic_editor = MagicMock()
    support_topic_repo = MagicMock()

    kwargs: dict[str, object] = {
        "support_chat_id": support_chat_id,
        "user_repo": user_repo,
        "forum_topic_creator": forum_topic_creator,
        "forum_topic_editor": forum_topic_editor,
        "support_topic_repo": support_topic_repo,
        "bot_name": bot_name,
    }
    if topic_name_format:
        kwargs["topic_name_format"] = topic_name_format

    manager = SupportTopicManager(**kwargs)  # type: ignore[arg-type]
    return manager, user_repo, forum_topic_creator, forum_topic_editor, support_topic_repo


class TestEnsureTopic:
    def test_returns_existing_topic(self) -> None:
        manager, _, _, _, support_topic_repo = _make_manager()
        support_topic_repo.find_by_user_and_chat.return_value = SupportTopic(
            user_id=123, chat_id=-1001234567890, topic_id=42
        )

        result = manager.ensure_topic(user_id=123)

        assert result == 42

    def test_creates_new_topic(self) -> None:
        manager, user_repo, forum_topic_creator, _, support_topic_repo = _make_manager()
        support_topic_repo.find_by_user_and_chat.return_value = None
        user_repo.get_by_id.return_value = _make_user()
        forum_topic_creator.create_topic.return_value = 99

        result = manager.ensure_topic(user_id=123)

        assert result == 99
        support_topic_repo.create.assert_called_once()
        created = support_topic_repo.create.call_args[1].get(
            "entity", support_topic_repo.create.call_args[0][0]
        )
        assert created.topic_id == 99

    def test_topic_name_uses_format(self) -> None:
        manager, user_repo, forum_topic_creator, _, support_topic_repo = _make_manager()
        support_topic_repo.find_by_user_and_chat.return_value = None
        user_repo.get_by_id.return_value = _make_user()
        forum_topic_creator.create_topic.return_value = 1

        manager.ensure_topic(user_id=123)

        call_args = forum_topic_creator.create_topic.call_args
        name = call_args.kwargs.get("name", call_args[1].get("name"))
        assert "TestBot" in name
        assert "John Doe" in name
        assert "+79991234567" in name
        assert "johndoe" in name


class TestUpdateTopicName:
    def test_updates_existing_topic(self) -> None:
        manager, user_repo, _, forum_topic_editor, support_topic_repo = _make_manager()
        support_topic_repo.find_by_user_and_chat.return_value = SupportTopic(
            user_id=123, chat_id=-1001234567890, topic_id=42
        )
        user_repo.get_by_id.return_value = _make_user(first_name="Jane")

        manager.update_topic_name(user_id=123)

        forum_topic_editor.edit_topic.assert_called_once()
        call_args = forum_topic_editor.edit_topic.call_args
        assert call_args.kwargs["topic_id"] == 42
        assert "Jane" in call_args.kwargs["name"]

    def test_skips_if_no_topic(self) -> None:
        manager, _, _, forum_topic_editor, support_topic_repo = _make_manager()
        support_topic_repo.find_by_user_and_chat.return_value = None

        manager.update_topic_name(user_id=123)

        forum_topic_editor.edit_topic.assert_not_called()


class TestTopicNameFormat:
    def test_custom_format(self) -> None:
        manager, user_repo, forum_topic_creator, _, support_topic_repo = _make_manager(
            topic_name_format="{full_name} ({username})"
        )
        support_topic_repo.find_by_user_and_chat.return_value = None
        user_repo.get_by_id.return_value = _make_user()
        forum_topic_creator.create_topic.return_value = 1

        manager.ensure_topic(user_id=123)

        call_args = forum_topic_creator.create_topic.call_args
        name = call_args.kwargs.get("name", call_args[1].get("name"))
        assert name == "John Doe (johndoe)"

    def test_missing_fields_use_unknown(self) -> None:
        manager, user_repo, forum_topic_creator, _, support_topic_repo = _make_manager()
        support_topic_repo.find_by_user_and_chat.return_value = None
        user_repo.get_by_id.return_value = _make_user(
            first_name=None, last_name=None, username=None, phone_number=None
        )
        forum_topic_creator.create_topic.return_value = 1

        manager.ensure_topic(user_id=123)

        call_args = forum_topic_creator.create_topic.call_args
        name = call_args.kwargs.get("name", call_args[1].get("name"))
        assert "Unknown" in name
        assert "unknown" in name

    def test_truncates_to_128_chars(self) -> None:
        manager, user_repo, forum_topic_creator, _, support_topic_repo = _make_manager(
            topic_name_format="{full_name}" + "x" * 200
        )
        support_topic_repo.find_by_user_and_chat.return_value = None
        user_repo.get_by_id.return_value = _make_user()
        forum_topic_creator.create_topic.return_value = 1

        manager.ensure_topic(user_id=123)

        call_args = forum_topic_creator.create_topic.call_args
        name = call_args.kwargs.get("name", call_args[1].get("name"))
        assert len(name) == 128
