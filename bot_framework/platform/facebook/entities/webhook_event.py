from pydantic import BaseModel


class WebhookSender(BaseModel):
    id: str


class QuickReply(BaseModel):
    payload: str


class WebhookAttachment(BaseModel):
    type: str
    payload: dict[str, str | int | None] | None = None


class WebhookMessage(BaseModel):
    mid: str
    text: str | None = None
    quick_reply: QuickReply | None = None
    attachments: list[WebhookAttachment] | None = None


class WebhookPostback(BaseModel):
    title: str
    payload: str


class WebhookEvent(BaseModel):
    sender: WebhookSender
    recipient: WebhookSender
    timestamp: int
    message: WebhookMessage | None = None
    postback: WebhookPostback | None = None


class WebhookEntry(BaseModel):
    id: str
    time: int
    messaging: list[WebhookEvent]


class WebhookPayload(BaseModel):
    object: str
    entry: list[WebhookEntry]
