from __future__ import annotations

from typing import Any

from bot_framework.core.entities.bot_user import BotUser
from bot_framework.core.protocols import IEnsureUserExists

MAX_DEFAULT_LANGUAGE_CODE = "ru"


class MaxEnsureUserMiddleware:
    def __init__(self, ensure_user_exists: IEnsureUserExists) -> None:
        self._ensure_user_exists = ensure_user_exists

    def execute_from_user_dict(self, user: dict[str, Any]) -> None:
        if not user:
            return
        bot_user = self._to_bot_user(user)
        self._ensure_user_exists.execute(user=bot_user)

    def _to_bot_user(self, user: dict[str, Any]) -> BotUser:
        bot_user = BotUser(
            id=int(user.get("user_id", 0)),
            username=user.get("username"),
            first_name=user.get("first_name") or user.get("name"),
            last_name=user.get("last_name"),
            language_code=MAX_DEFAULT_LANGUAGE_CODE,
            is_bot=bool(user.get("is_bot", False)),
            is_premium=False,
        )
        bot_user.set_original(user)
        return bot_user
