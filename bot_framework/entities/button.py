from pydantic import BaseModel, ConfigDict


class Button(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    callback_data: str
