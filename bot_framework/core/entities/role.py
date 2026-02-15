from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class Role(BaseModel):
    id: int = 0
    name: str
    description: str | None = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
