from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from bot_framework.domain.flow_management import RedisFlowMessageStorage
from bot_framework.features.flows.request_role_flow import RequestRoleFlowFactory
from bot_framework.features.flows.request_role_flow.repos import (
    RedisRequestRoleFlowStateStorage,
)
from bot_framework.domain.language_management.loaders import (
    LanguageLoader,
    PhraseLoader,
)
from bot_framework.domain.language_management.repos import LanguageRepo
from bot_framework.domain.language_management.validators import (
    MissingTranslationsValidator,
)
from bot_framework.domain.role_management.loaders import RoleLoader
from bot_framework.domain.language_management.providers import RedisPhraseProvider
from bot_framework.features.menus import (
    MainMenuSender,
    MenuButtonConfig,
    StartCommandHandler,
)
from bot_framework.features.menus.language_menu import LanguageMenuFactory
from bot_framework.core.protocols.i_callback_handler import ICallbackHandler
from bot_framework.domain.role_management.repos import RoleRepo, UserRepo
from bot_framework.platform.telegram import CloseCallbackHandler, TelegramMessageCore

if TYPE_CHECKING:
    from telebot import TeleBot

    from bot_framework.platform.telegram.services import (
        CallbackAnswerer,
        CallbackHandlerRegistry,
        NextStepHandlerRegistrar,
        TelegramMessenger,
    )


class BotApplication:
    def __init__(
        self,
        bot_token: str,
        database_url: str,
        redis_url: str,
        phrases_json_path: Path | None = None,
        languages_json_path: Path | None = None,
        roles_json_path: Path | None = None,
        use_class_middlewares: bool = True,
        auto_migrate: bool = True,
        support_chat_id: int | None = None,
    ) -> None:
        if auto_migrate:
            from bot_framework.app.migrations import apply_migrations

            apply_migrations(database_url)

        self._load_roles(database_url, roles_json_path)
        self._load_languages(redis_url, database_url, languages_json_path)
        self._load_phrases(redis_url, phrases_json_path)
        self._validate_translations(languages_json_path, phrases_json_path)

        flow_message_storage = RedisFlowMessageStorage(redis_url=redis_url)
        self.core = TelegramMessageCore(
            bot_token=bot_token,
            database_url=database_url,
            flow_message_storage=flow_message_storage,
            use_class_middlewares=use_class_middlewares,
        )

        self._database_url = database_url
        self.user_repo = UserRepo(database_url=database_url)
        self.role_repo = RoleRepo(database_url=database_url)
        self.phrase_provider = RedisPhraseProvider(redis_url=redis_url)
        self.phrase_repo = self.phrase_provider  # обратная совместимость

        if support_chat_id:
            self._setup_support_chat(support_chat_id)

        self._setup_menus(redis_url)

    def _setup_support_chat(self, support_chat_id: int) -> None:
        from bot_framework.domain.support_chat.services import SupportTopicManager
        from bot_framework.platform.telegram.handlers import StaffReplyHandler
        from bot_framework.platform.telegram.middleware import SupportChatMiddleware
        from bot_framework.platform.telegram.services.support_mirror_messenger import (
            SupportMirrorMessenger,
        )
        from bot_framework.platform.telegram.services.telegram_forum_topic_creator import (
            TelegramForumTopicCreator,
        )

        forum_topic_creator = TelegramForumTopicCreator(
            raw_forum_topic_creator=self.core.raw_forum_topic_creator,
        )
        topic_manager = SupportTopicManager(
            support_chat_id=support_chat_id,
            user_repo=self.user_repo,
            forum_topic_creator=forum_topic_creator,
        )

        mirror = SupportMirrorMessenger(
            messenger=self.core.message_sender,
            thread_message_sender=self.core.thread_message_sender,
            support_chat_id=support_chat_id,
            support_topic_manager=topic_manager,
            user_repo=self.user_repo,
            phrase_repo=self.phrase_provider,
        )
        self.core.message_sender = mirror  # type: ignore[assignment]
        self.core.message_replacer = mirror  # type: ignore[assignment]
        self.core.document_sender = mirror  # type: ignore[assignment]

        middleware = SupportChatMiddleware(
            support_chat_id=support_chat_id,
            support_topic_manager=topic_manager,
            message_forwarder=self.core.message_forwarder,
        )
        self.core.middleware_setup.setup_middleware(middleware)

        staff_handler = StaffReplyHandler(
            thread_message_sender=self.core.thread_message_sender,
            user_repo=self.user_repo,
            phrase_repo=self.phrase_provider,
            support_chat_id=support_chat_id,
        )
        self.core.message_handler_registry.register(
            handler=staff_handler,
            func=lambda m: m.chat.id == support_chat_id,
            content_types=["text"],
        )

    def _load_languages(
        self,
        redis_url: str,
        database_url: str,
        client_languages_path: Path | None,
    ) -> None:
        loader = LanguageLoader(redis_url=redis_url, database_url=database_url)
        data_dir = Path(__file__).parent.parent / "data"

        base_path = data_dir / "languages.json"
        if base_path.exists():
            loader.load_from_json(base_path)

        if client_languages_path and client_languages_path.exists():
            loader.load_from_json(client_languages_path)

    def _load_phrases(
        self,
        redis_url: str,
        client_phrases_path: Path | None,
    ) -> None:
        loader = PhraseLoader(redis_url=redis_url)
        data_dir = Path(__file__).parent.parent / "data"

        base_path = data_dir / "phrases.json"
        if base_path.exists():
            loader.load_from_json(base_path)

        if client_phrases_path and client_phrases_path.exists():
            loader.load_from_json(client_phrases_path)

    def _load_roles(
        self,
        database_url: str,
        client_roles_path: Path | None,
    ) -> None:
        loader = RoleLoader(database_url=database_url)
        data_dir = Path(__file__).parent.parent / "data"

        base_path = data_dir / "roles.json"
        if base_path.exists():
            loader.load_from_json(base_path)

        if client_roles_path and client_roles_path.exists():
            loader.load_from_json(client_roles_path)

    def _validate_translations(
        self,
        client_languages_path: Path | None,
        client_phrases_path: Path | None,
    ) -> None:
        data_dir = Path(__file__).parent.parent / "data"
        validator = MissingTranslationsValidator()
        validator.validate_and_log_missing(
            library_languages_path=data_dir / "languages.json",
            library_phrases_path=data_dir / "phrases.json",
            client_languages_path=client_languages_path,
            client_phrases_path=client_phrases_path,
        )

    def _setup_menus(self, redis_url: str) -> None:
        self._close_handler = CloseCallbackHandler(
            callback_answerer=self.core.callback_answerer,
            message_deleter=self.core.message_deleter,
        )
        self.core.callback_handler_registry.register(self._close_handler)

        request_role_flow_state_storage = RedisRequestRoleFlowStateStorage(
            redis_url=redis_url,
        )

        request_role_flow_factory = RequestRoleFlowFactory(
            callback_answerer=self.core.callback_answerer,
            message_sender=self.core.message_sender,
            phrase_repo=self.phrase_repo,
            role_repo=self.role_repo,
            user_repo=self.user_repo,
            state_storage=request_role_flow_state_storage,
        )

        request_role_flow_factory.register_handlers(
            callback_registry=self.core.callback_handler_registry,
            message_registry=self.core.message_handler_registry,
        )
        request_role_flow_router = request_role_flow_factory.create_router()

        self._main_menu_sender = MainMenuSender(
            message_sender=self.core.message_sender,
            phrase_repo=self.phrase_repo,
            role_repo=self.role_repo,
            welcome_phrase_key="bot.start.welcome",
            buttons=[],
        )

        self._start_command_handler = StartCommandHandler(
            user_repo=self.user_repo,
            role_repo=self.role_repo,
            main_menu_sender=self._main_menu_sender,
            request_role_flow_router=request_role_flow_router,
            message_sender=self.core.message_sender,
        )

        self.core.message_handler_registry.register(
            handler=self._start_command_handler,
            commands=["start"],
            content_types=["text"],
        )

        language_menu_factory = LanguageMenuFactory(
            callback_answerer=self.core.callback_answerer,
            message_sender=self.core.message_sender,
            message_replacer=self.core.message_replacer,
            phrase_repo=self.phrase_repo,
            language_repo=LanguageRepo(database_url=self._database_url),
            user_repo=self.user_repo,
        )
        language_menu_factory.register_handlers(
            callback_registry=self.core.callback_handler_registry,
            message_registry=self.core.message_handler_registry,
        )

    def add_main_menu_button(
        self,
        phrase_key: str,
        handler: ICallbackHandler,
    ) -> None:
        config = MenuButtonConfig(phrase_key=phrase_key, handler=handler)
        self._main_menu_sender.buttons.insert(0, config)

    def set_start_allowed_roles(self, roles: set[str]) -> None:
        self._start_command_handler.allowed_roles = roles

    @property
    def bot(self) -> TeleBot:  # noqa: F821
        return self.core.bot

    @property
    def message_sender(self) -> TelegramMessenger:  # noqa: F821
        return self.core.message_sender

    @property
    def message_replacer(self) -> TelegramMessenger:  # noqa: F821
        return self.core.message_replacer

    @property
    def message_deleter(self) -> TelegramMessenger:  # noqa: F821
        return self.core.message_deleter

    @property
    def document_sender(self) -> TelegramMessenger:  # noqa: F821
        return self.core.document_sender

    @property
    def callback_handler_registry(self) -> CallbackHandlerRegistry:  # noqa: F821
        return self.core.callback_handler_registry

    @property
    def callback_answerer(self) -> CallbackAnswerer:  # noqa: F821
        return self.core.callback_answerer

    @property
    def next_step_registrar(self) -> NextStepHandlerRegistrar:  # noqa: F821
        return self.core.next_step_registrar

    @property
    def close_handler(self) -> CloseCallbackHandler:
        return self._close_handler

    def run(self) -> None:
        self.core.polling_bot.infinity_polling()
