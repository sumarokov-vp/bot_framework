from collections.abc import Callable
from functools import wraps
from typing import Any

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.entities.bot_message import BotMessage

CallbackHandler = Callable[[Any, BotCallback], None]
MessageHandler = Callable[[Any, BotMessage], None]


class OperationNotAllowedError(Exception):
    pass


def check_roles[T: CallbackHandler](func: T) -> T:
    @wraps(func)
    def wrapper(self: Any, callback: BotCallback) -> None:
        if hasattr(self, "allowed_roles") and self.allowed_roles:
            if not callback.user_id:
                raise ValueError("callback.user_id is required but was None")

            telegram_id = callback.user_id
            user_roles = self.role_repo.get_user_roles(user_id=telegram_id)
            user_role_names = {role.name for role in user_roles}

            if not (user_role_names & self.allowed_roles):
                if hasattr(self, "callback_answerer"):
                    self.callback_answerer.answer(
                        callback_query_id=callback.id,
                        text=f"You do not have the required roles: {self.allowed_roles}",
                        show_alert=True,
                    )
                raise OperationNotAllowedError(
                    f"User {telegram_id} does not have required roles: {self.allowed_roles}"
                )

        return func(self, callback)

    return wrapper  # type: ignore[return-value]


def check_message_roles[M: MessageHandler](func: M) -> M:
    @wraps(func)
    def wrapper(self: Any, message: BotMessage) -> None:
        if hasattr(self, "allowed_roles") and self.allowed_roles:
            if not message.from_user:
                raise ValueError("message.from_user is required but was None")

            telegram_id = message.from_user.id
            user_roles = self.role_repo.get_user_roles(user_id=telegram_id)
            user_role_names = {role.name for role in user_roles}

            if not (user_role_names & self.allowed_roles):
                if hasattr(self, "request_role_flow_router") and hasattr(
                    self, "user_repo"
                ):
                    user = self.user_repo.get_by_id(id=telegram_id)
                    self.request_role_flow_router.start(user)
                    return
                if hasattr(self, "message_sender") and self.message_sender:
                    self.message_sender.send(
                        chat_id=message.chat_id,
                        text=f"You do not have the required roles: {self.allowed_roles}",
                    )
                raise OperationNotAllowedError(
                    f"User {telegram_id} does not have required roles: {self.allowed_roles}"
                )

        return func(self, message)

    return wrapper  # type: ignore[return-value]
