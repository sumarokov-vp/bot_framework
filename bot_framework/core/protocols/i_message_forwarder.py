from typing import Any, Protocol


class IMessageForwarder(Protocol):
    def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        timeout: int | None = None,
        message_thread_id: int | None = None,
    ) -> Any: ...
