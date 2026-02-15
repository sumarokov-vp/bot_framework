from __future__ import annotations

from typing import TYPE_CHECKING

from telebot.handler_backends import BaseMiddleware

if TYPE_CHECKING:
    from bot_framework.core.protocols.i_middleware_setup import IMiddlewareSetup


class TelegramBaseMiddleware(BaseMiddleware):
    def register(self, middleware_setup: IMiddlewareSetup) -> None:
        middleware_setup.setup_middleware(self)
