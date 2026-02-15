from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr


class BotMessageUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BotMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: int
    message_id: int
    user_id: int | None = None
    text: str | None = None
    from_user: BotMessageUser | None = None
    document_file_id: str | None = None
    message_thread_id: int | None = None
    _original: Any = PrivateAttr(default=None)

    def get_original(self) -> Any:
        return self._original

    def set_original(self, original: Any) -> None:
        self._original = original
