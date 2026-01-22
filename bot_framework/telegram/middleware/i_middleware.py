from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware


class IMiddleware(BaseMiddleware):
    def register(self, bot: TeleBot) -> None:
        bot.setup_middleware(self)
