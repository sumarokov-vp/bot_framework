from typing import Protocol


class IMessageDeleter(Protocol):
    def delete(self, chat_id: int, message_id: int) -> None: ...
