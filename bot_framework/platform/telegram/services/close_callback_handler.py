from bot_framework.core.entities.bot_callback import BotCallback
from bot_framework.platform.telegram.protocols import ICallbackAnswerer, IMessageDeleter


class CloseCallbackHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        message_deleter: IMessageDeleter,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.message_deleter = message_deleter
        self.allowed_roles: set[str] | None = None
        self.prefix = "close:"

    def handle(self, callback: BotCallback) -> None:
        if not callback.message_id or not callback.message_chat_id:
            self.callback_answerer.answer(callback.id)
            return

        self.message_deleter.delete(
            chat_id=callback.message_chat_id,
            message_id=callback.message_id,
        )
        self.callback_answerer.answer(callback.id)
