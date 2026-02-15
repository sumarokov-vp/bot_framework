from typing import Protocol


class IPollingBot(Protocol):
    def infinity_polling(self) -> None: ...
