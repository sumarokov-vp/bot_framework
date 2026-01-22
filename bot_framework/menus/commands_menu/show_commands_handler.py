from uuid import uuid4

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.menus.commands_menu.i_commands_menu_sender import ICommandsMenuSender
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer


class ShowCommandsHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        commands_menu_sender: ICommandsMenuSender,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.commands_menu_sender = commands_menu_sender
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.message_chat_id:
            raise ValueError("callback.message_chat_id is required but was None")

        language_code = callback.user_language_code or "en"
        self.commands_menu_sender.send(
            chat_id=callback.message_chat_id,
            language_code=language_code,
        )
