from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr


class BotCallback(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: int
    data: str | None
    message_id: int | None
    message_chat_id: int | None
    user_language_code: str | None = None
    _original: Any = PrivateAttr(default=None)

    def get_original(self) -> Any:
        return self._original

    def set_original(self, original: Any) -> None:
        self._original = original
