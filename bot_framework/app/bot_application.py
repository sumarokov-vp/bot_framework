from __future__ import annotations

from typing import TYPE_CHECKING

from bot_framework.flow_management import RedisFlowMessageStorage
from bot_framework.flows.request_role_flow import RequestRoleFlowFactory
from bot_framework.flows.request_role_flow.repos import (
    RedisRequestRoleFlowStateStorage,
)
from bot_framework.language_management.repos import PhraseRepo
from bot_framework.menus import (
    CommandsMenuSender,
    MainMenuSender,
    MenuButtonConfig,
    ShowCommandsHandler,
    StartCommandHandler,
)
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
    )


class BotApplication:
    def __init__(
        self,
        bot_token: str,
        database_url: str,
        redis_url: str,
        use_class_middlewares: bool = False,
    ) -> None:
        flow_message_storage = RedisFlowMessageStorage(redis_url=redis_url)
        self.core = TelegramMessageCore(
            bot_token=bot_token,
            database_url=database_url,
            flow_message_storage=flow_message_storage,
            use_class_middlewares=use_class_middlewares,
        )

        self.user_repo = UserRepo(database_url=database_url)
        self.role_repo = RoleRepo(database_url=database_url)
        self.phrase_repo = PhraseRepo(database_url=database_url)

        self._setup_menus(redis_url)

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
