from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr


class BotUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str
    is_bot: bool
    is_premium: bool
    _original: Any = PrivateAttr(default=None)

    def get_original(self) -> Any:
        return self._original

    def set_original(self, original: Any) -> None:
        self._original = original
