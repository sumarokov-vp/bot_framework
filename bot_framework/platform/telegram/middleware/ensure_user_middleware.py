from telebot.types import CallbackQuery, Message, User as TelegramUser

from bot_framework.core.entities.bot_user import BotUser
from bot_framework.core.protocols import IEnsureUserExists
from bot_framework.platform.telegram.middleware.telegram_base_middleware import (
    TelegramBaseMiddleware,
)


class EnsureUserMiddleware(TelegramBaseMiddleware):
    update_types = ["message", "callback_query"]

    def __init__(self, ensure_user_exists: IEnsureUserExists):
        super().__init__()
        self.ensure_user_exists = ensure_user_exists
        self.update_sensitive = False

    def pre_process(
        self,
        message: Message | CallbackQuery,
        data: dict[str, object],
    ) -> None:
        telegram_user = message.from_user
        if not telegram_user:
            return
        bot_user = self._to_bot_user(telegram_user)
        self.ensure_user_exists.execute(user=bot_user)

    def _to_bot_user(self, telegram_user: TelegramUser) -> BotUser:
        bot_user = BotUser(
            id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            language_code=telegram_user.language_code or "en",
            is_bot=telegram_user.is_bot,
            is_premium=telegram_user.is_premium or False,
        )
        bot_user.set_original(telegram_user)
        return bot_user

    def post_process(
        self,
        message: Message | CallbackQuery,
        data: dict[str, object],
        exception: Exception | None,
    ) -> None:
        pass
