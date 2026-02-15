from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class UserRole(BaseModel):
    user_id: int
    role_id: int
    assigned_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
