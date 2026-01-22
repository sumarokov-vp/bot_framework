from datetime import datetime

from pydantic import (
    BaseModel, ConfigDict, Field,
)


class Language(BaseModel):
    code: str
    name: str
    native_name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
