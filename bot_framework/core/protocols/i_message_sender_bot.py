from typing import Any, Protocol


class IMessageSenderBot(Protocol):
    def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str | None = None,
        reply_markup: Any = None,
        message_thread_id: int | None = None,
    ) -> Any: ...

    def edit_message_text(
        self,
        text: str,
        chat_id: int,
        message_id: int,
        parse_mode: str | None = None,
        reply_markup: Any = None,
    ) -> Any: ...

    def delete_message(self, chat_id: int, message_id: int) -> bool: ...

    def send_document(
        self,
        chat_id: int,
        document: Any,
    ) -> Any: ...
