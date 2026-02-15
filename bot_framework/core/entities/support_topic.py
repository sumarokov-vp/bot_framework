from pydantic import BaseModel, ConfigDict


class SupportTopic(BaseModel):
    user_id: int
    chat_id: int
    topic_id: int

    model_config = ConfigDict(from_attributes=True)
