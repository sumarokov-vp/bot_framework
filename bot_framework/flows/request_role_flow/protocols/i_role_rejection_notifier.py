from typing import Protocol


class IRoleRejectionNotifier(Protocol):
    def notify(
        self,
        user_id: int,
        language_code: str,
    ) -> None: ...
