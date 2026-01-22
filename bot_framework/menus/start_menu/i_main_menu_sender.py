from typing import Protocol


class IMainMenuSender(Protocol):
    def send(self, chat_id: int, language_code: str) -> None: ...
