from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from bot_framework.core.entities.language_code import LanguageCode


class User(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str = LanguageCode.EN
    is_bot: bool = False
    is_premium: bool = False
    support_chat_id: int | None = None
    support_topic_id: int | None = None
    party_id: int | None = None
    last_rejection_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
