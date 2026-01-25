from uuid import uuid4

from bot_framework.entities.bot_callback import BotCallback
from bot_framework.language_management.repos.protocols.i_phrase_repo import IPhraseRepo
from bot_framework.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.protocols.i_message_sender import IMessageSender
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class SelectLanguageHandler:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        user_repo: IUserRepo,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.user_repo = user_repo
        self.prefix = uuid4().hex
        self.allowed_roles: set[str] | None = None

    def handle(self, callback: BotCallback) -> None:
        self.callback_answerer.answer(callback_query_id=callback.id)

        if not callback.data:
            raise ValueError("callback.data is required but was None")

        parts = callback.data.split(":")
        if len(parts) < 2:
            raise ValueError(f"Invalid callback data format: {callback.data}")

        new_language_code = parts[1]

        self.user_repo.update_language(
            user_id=callback.user_id,
            language_code=new_language_code,
        )

        text = self.phrase_repo.get_phrase(
            key="language.changed",
            language_code=new_language_code,
        )
        self.message_sender.send(chat_id=callback.user_id, text=text)
