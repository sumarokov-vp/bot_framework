from __future__ import annotations

from typing import TYPE_CHECKING

from bot_framework.platform.max.repos import MaxDialogRepo

from .services.max_api_client import MaxApiClient
from .services.max_callback_answerer import MaxCallbackAnswerer
from .services.max_callback_handler_registry import MaxCallbackHandlerRegistry
from .services.max_message_core import MaxMessageCore
from .services.max_message_handler_registry import MaxMessageHandlerRegistry
from .services.max_messenger import MaxMessenger
from .services.max_mid_registry import MaxMidRegistry
from .services.max_next_step_handler_registrar import MaxNextStepHandlerRegistrar
from .services.max_polling import MaxPolling

if TYPE_CHECKING:
    from bot_framework.domain.flow_management.protocols.i_flow_message_storage import (
        IFlowMessageStorage,
    )
    from bot_framework.platform.max.middleware.ensure_user_middleware import (
        MaxEnsureUserMiddleware,
    )


class MaxDialogs:
    def __init__(
        self,
        token: str,
        database_url: str,
        flow_message_storage: IFlowMessageStorage | None = None,
        ensure_user_middleware: MaxEnsureUserMiddleware | None = None,
    ) -> None:
        api_client = MaxApiClient(token)
        dialog_repo = MaxDialogRepo(database_url=database_url)
        mid_registry = MaxMidRegistry()

        core = MaxMessageCore(
            api_client=api_client,
            dialog_repo=dialog_repo,
            mid_registry=mid_registry,
            flow_message_storage=flow_message_storage,
            ensure_user_middleware=ensure_user_middleware,
        )

        messenger = MaxMessenger(core)
        core.setup(
            messenger=messenger,
            callback_answerer=MaxCallbackAnswerer(core),
            callback_handler_registry=MaxCallbackHandlerRegistry(),
            message_handler_registry=MaxMessageHandlerRegistry(),
            next_step_registrar=MaxNextStepHandlerRegistrar(),
            polling=MaxPolling(core),
        )

        self.core = core
