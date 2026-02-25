from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .max_message_core import MaxMessageCore

logger = getLogger(__name__)

BOT_STARTED_COMMAND = "/start"


class MaxPolling:
    def __init__(self, core: MaxMessageCore) -> None:
        self._core = core
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
        update_type = update.get("update_type")

        if update_type == "message_created":
            self._handle_message_created(update)
        elif update_type == "message_callback":
            self._handle_message_callback(update)
        elif update_type == "bot_started":
            self._handle_bot_started(update)
        else:
            self._logger.debug("Unhandled update type: %s", update_type)

    def _handle_message_created(self, update: dict[str, Any]) -> None:
        message = update.get("message", {})
        body = message.get("body", {}) or message.get("message", {})
        raw_mid = body.get("mid", "")

        self._core.register_mid(raw_mid)

        if self._core.ensure_user_middleware:
            sender = message.get("sender", {})
            self._core.ensure_user_middleware.execute_from_user_dict(sender)

        sender = message.get("sender", {})
        recipient = message.get("recipient", {})
        user_id = int(sender.get("user_id", 0))
        chat_id = int(recipient.get("chat_id", 0))
        if user_id and chat_id:
            self._core.dialog_repo.upsert(user_id=user_id, chat_id=chat_id)
        next_step_handler = self._core.next_step_registrar.pop(user_id)
        if next_step_handler is not None:
            bot_message = self._core.next_step_registrar.to_bot_message(
                update,
                self._core.mid_to_int,
            )
            next_step_handler.handle(bot_message)
            return

        text = body.get("text")
        if not text and not raw_mid:
            self._core.message_handler_registry.dispatch(
                update,
                self._core.mid_to_int,
                command_override=BOT_STARTED_COMMAND,
            )
            return

        self._core.message_handler_registry.dispatch(
            update,
            self._core.mid_to_int,
        )

    def _handle_message_callback(self, update: dict[str, Any]) -> None:
        message = update.get("message", {})
        body = message.get("body", {}) or message.get("message", {})
        raw_mid = body.get("mid", "")

        self._core.register_mid(raw_mid)

        if self._core.ensure_user_middleware:
            callback = update.get("callback", {})
            user = callback.get("user", {})
            self._core.ensure_user_middleware.execute_from_user_dict(user)

        self._core.callback_handler_registry.dispatch(update, self._core.mid_to_int)

    def _handle_bot_started(self, update: dict[str, Any]) -> None:
        user = update.get("user", {})

        if self._core.ensure_user_middleware:
            self._core.ensure_user_middleware.execute_from_user_dict(user)

        user_id = int(user.get("user_id", 0))
        chat_id = int(update.get("chat_id", 0))
        if user_id and chat_id:
            self._core.dialog_repo.upsert(user_id=user_id, chat_id=chat_id)

        synthetic_update = self._build_synthetic_message_update(update, user)
        self._core.message_handler_registry.dispatch(
            synthetic_update,
            self._core.mid_to_int,
            command_override=BOT_STARTED_COMMAND,
        )

    def _build_synthetic_message_update(
        self,
        update: dict[str, Any],
        user: dict[str, Any],
    ) -> dict[str, Any]:
        chat_id = update.get("chat_id")
        user_id = user.get("user_id")
        return {
            "update_type": "message_created",
            "timestamp": update.get("timestamp", 0),
            "message": {
                "sender": user,
                "recipient": {
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "chat_type": "dialog",
                },
                "body": {
                    "mid": "",
                    "text": BOT_STARTED_COMMAND,
                },
            },
        }
