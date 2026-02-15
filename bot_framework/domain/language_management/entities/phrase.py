from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class Phrase(BaseModel):
    id: int = 0
    key: str
    language_code: str
    text: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
