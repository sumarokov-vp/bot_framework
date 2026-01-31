from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from bot_framework.flow_management import RedisFlowMessageStorage
from bot_framework.flows.request_role_flow import RequestRoleFlowFactory
from bot_framework.flows.request_role_flow.repos import (
    RedisRequestRoleFlowStateStorage,
)
from bot_framework.language_management.loaders import LanguageLoader, PhraseLoader
from bot_framework.language_management.repos import LanguageRepo
from bot_framework.language_management.validators import MissingTranslationsValidator
from bot_framework.role_management.loaders import RoleLoader
from bot_framework.language_management.providers import RedisPhraseProvider
from bot_framework.menus import (
    CommandsMenuSender,
    MainMenuSender,
    MenuButtonConfig,
    ShowCommandsHandler,
    StartCommandHandler,
)
from bot_framework.menus.language_menu import LanguageMenuFactory
from bot_framework.protocols.i_callback_handler import ICallbackHandler
from bot_framework.role_management.repos import RoleRepo, UserRepo
from bot_framework.telegram import CloseCallbackHandler, TelegramMessageCore

if TYPE_CHECKING:
    from telebot import TeleBot

    from bot_framework.telegram.services import (
        CallbackAnswerer,
        CallbackHandlerRegistry,
        NextStepHandlerRegistrar,
        TelegramMessageDeleter,
        TelegramMessageReplacer,
        TelegramMessageSender,
        TelegramMessageService,
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
    ) -> None:
        if auto_migrate:
            from bot_framework.migrations import apply_migrations

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

        self._setup_menus(redis_url)

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

        self._commands_menu_sender = CommandsMenuSender(
            message_sender=self.core.message_sender,
            phrase_repo=self.phrase_repo,
            title_phrase_key="commands.list_title",
        )

        self._show_commands_handler = ShowCommandsHandler(
            callback_answerer=self.core.callback_answerer,
            commands_menu_sender=self._commands_menu_sender,
            user_repo=self.user_repo,
        )
        self.core.callback_handler_registry.register(self._show_commands_handler)

        self._main_menu_sender = MainMenuSender(
            message_sender=self.core.message_sender,
            phrase_repo=self.phrase_repo,
            welcome_phrase_key="bot.start.welcome",
            buttons=[
                MenuButtonConfig(
                    phrase_key="commands.menu_button",
                    handler=self._show_commands_handler,
                ),
            ],
        )

        start_command_handler = StartCommandHandler(
            user_repo=self.user_repo,
            role_repo=self.role_repo,
            main_menu_sender=self._main_menu_sender,
            request_role_flow_router=request_role_flow_router,
        )

        self.core.message_handler_registry.register(
            handler=start_command_handler,
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

    def add_commands_button(
        self,
        phrase_key: str,
        handler: ICallbackHandler,
    ) -> None:
        self._commands_menu_sender.add_button(
            MenuButtonConfig(phrase_key=phrase_key, handler=handler)
        )

    @property
    def bot(self) -> TeleBot:  # noqa: F821
        return self.core.bot

    @property
    def message_sender(self) -> TelegramMessageSender:  # noqa: F821
        return self.core.message_sender

    @property
    def message_replacer(self) -> TelegramMessageReplacer:  # noqa: F821
        return self.core.message_replacer

    @property
    def message_deleter(self) -> TelegramMessageDeleter:  # noqa: F821
        return self.core.message_deleter

    @property
    def message_service(self) -> TelegramMessageService:  # noqa: F821
        return self.core.message_service

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
        self.core.bot.infinity_polling()
