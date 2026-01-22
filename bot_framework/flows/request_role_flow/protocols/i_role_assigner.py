from typing import Protocol


class IRoleAssigner(Protocol):
    def assign_and_notify(
        self,
        user_id: int,
        role_id: int,
        language_code: str,
    ) -> None: ...
