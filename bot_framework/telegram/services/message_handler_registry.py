from collections.abc import Callable

from telebot import TeleBot
from telebot.types import Message

from bot_framework.entities.bot_message import BotMessage, BotMessageUser
from bot_framework.protocols.i_message_handler import IMessageHandler


class MessageHandlerRegistry:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def register(
        self,
        handler: IMessageHandler,
        commands: list[str] | None = None,
        content_types: list[str] | None = None,
        func: Callable[[Message], bool] | None = None,
    ) -> None:
        def wrapper(message: Message) -> bool | None:
            bot_message = self._to_bot_message(message)
            return handler.handle(bot_message)

        self.bot.register_message_handler(
            callback=wrapper,
            commands=commands,
            content_types=content_types,
            func=func,
        )

    def _to_bot_message(self, message: Message) -> BotMessage:
        if not message.from_user:
            raise ValueError("message.from_user is required but was None")

        from_user = BotMessageUser(
            id=message.from_user.id,
            language_code=message.from_user.language_code,
        )

        bot_message = BotMessage(
            chat_id=message.chat.id,
            message_id=message.message_id,
            user_id=message.from_user.id,
            text=message.text,
            from_user=from_user,
        )
        bot_message.set_original(message)
        return bot_message
