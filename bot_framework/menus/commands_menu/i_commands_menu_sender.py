from typing import Protocol


class ICommandsMenuSender(Protocol):
    def send(self, chat_id: int, language_code: str) -> None: ...
