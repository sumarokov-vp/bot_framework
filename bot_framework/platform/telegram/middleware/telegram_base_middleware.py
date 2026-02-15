from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware


class TelegramBaseMiddleware(BaseMiddleware):
    """Telegram-specific base middleware class.

    Extends telebot's BaseMiddleware for use with Telegram bots.
    """

    def register(self, bot: TeleBot) -> None:
        bot.setup_middleware(self)
