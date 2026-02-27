from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from .max_update_parser import MaxParsedUpdate, MaxUpdateParser

if TYPE_CHECKING:
    from .max_message_core import MaxMessageCore

logger = getLogger(__name__)


class MaxPolling:
    def __init__(self, core: MaxMessageCore) -> None:
        self._core = core
        self._parser = MaxUpdateParser()
        self._marker: int | None = None
        self._logger = getLogger(__name__)

    def run(self) -> None:
        self._logger.info("Max polling started")
        while True:
            self._poll_once()

    def _poll_once(self) -> None:
        result = self._core.api_client.get_updates(
            limit=50,
            timeout=30,
            marker=self._marker,
        )
        marker = result.get("marker")
        if marker is not None:
            self._marker = marker

        updates: list[dict[str, Any]] = result.get("updates", [])
        for update in updates:
            self._dispatch(update)

    def _dispatch(self, update: dict[str, Any]) -> None:
        parsed = self._parser.parse(update)

        if parsed.update_type == "message_created":
            self._handle_message_created(parsed)
        elif parsed.update_type == "message_callback":
            self._handle_message_callback(parsed)
        elif parsed.update_type == "bot_started":
            self._handle_bot_started(parsed)
        else:
            self._logger.debug("Unhandled update type: %s", parsed.update_type)

    def _handle_message_created(self, parsed: MaxParsedUpdate) -> None:
        self._core.register_mid(parsed.mid)

        if self._core.ensure_user_middleware:
            self._core.ensure_user_middleware.execute_from_user_dict(parsed.sender)

        user_id = int(parsed.sender.get("user_id", 0))
        chat_id = int(parsed.recipient.get("chat_id", 0))
        if user_id and chat_id:
            self._core.dialog_repo.upsert(user_id=user_id, chat_id=chat_id)

        next_step_handler = self._core.next_step_registrar.pop(user_id)
        if next_step_handler is not None:
            bot_message = self._core.next_step_registrar.to_bot_message(
                parsed.raw_update,
                self._core.mid_to_int,
            )
            next_step_handler.handle(bot_message)
            return

        self._core.message_handler_registry.dispatch(
            parsed.raw_update,
            self._core.mid_to_int,
            command_override=parsed.command,
        )

    def _handle_message_callback(self, parsed: MaxParsedUpdate) -> None:
        self._core.register_mid(parsed.mid)

        if self._core.ensure_user_middleware:
            self._core.ensure_user_middleware.execute_from_user_dict(parsed.sender)

        self._core.callback_handler_registry.dispatch(parsed.raw_update, self._core.mid_to_int)

    def _handle_bot_started(self, parsed: MaxParsedUpdate) -> None:
        if self._core.ensure_user_middleware:
            self._core.ensure_user_middleware.execute_from_user_dict(parsed.sender)

        user_id = int(parsed.sender.get("user_id", 0))
        chat_id = int(parsed.recipient.get("chat_id", 0))
        if user_id and chat_id:
            self._core.dialog_repo.upsert(user_id=user_id, chat_id=chat_id)

        self._core.message_handler_registry.dispatch(
            parsed.raw_update,
            self._core.mid_to_int,
            command_override=parsed.command,
        )
