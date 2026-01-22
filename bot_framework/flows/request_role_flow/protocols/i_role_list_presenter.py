from typing import Protocol


class IRoleListPresenter(Protocol):
    def present(self, chat_id: int, user_id: int, language_code: str) -> None: ...
