from telebot import TeleBot


class CallbackAnswerer:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def answer(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool = False,
    ) -> None:
        self.bot.answer_callback_query(
            callback_query_id, text=text, show_alert=show_alert  # pyright: ignore[reportArgumentType]
        )
