from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from bot_framework.entities.language_code import LanguageCode


class User(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str = LanguageCode.EN
    is_bot: bool = False
    is_premium: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
