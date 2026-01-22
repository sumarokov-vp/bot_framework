from pydantic import BaseModel, ConfigDict

from bot_framework.entities.button import Button


class Keyboard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rows: list[list[Button]]
