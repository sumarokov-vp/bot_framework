from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from bot_framework.platform.facebook.entities.webhook_event import WebhookEvent, WebhookPayload

if TYPE_CHECKING:
    from .message_handler_registry import FacebookMessageHandlerRegistry
    from .postback_handler_registry import PostbackHandlerRegistry


class FacebookWebhookServer:
    def __init__(
        self,
        verify_token: str,
        postback_registry: PostbackHandlerRegistry,
        message_registry: FacebookMessageHandlerRegistry,
    ) -> None:
        self._verify_token = verify_token
        self._postback_registry = postback_registry
        self._message_registry = message_registry
        self._logger = getLogger(__name__)
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self) -> None:
        @self.app.get("/webhook")
        async def verify(request: Request) -> PlainTextResponse:
            params = request.query_params
            mode = params.get("hub.mode")
            token = params.get("hub.verify_token")
            challenge = params.get("hub.challenge")

            if mode == "subscribe" and token == self._verify_token:
                return PlainTextResponse(content=challenge or "")
            return PlainTextResponse(content="Forbidden", status_code=403)

        @self.app.post("/webhook")
        async def webhook(request: Request) -> PlainTextResponse:
            body = await request.json()
            payload = WebhookPayload.model_validate(body)

            if payload.object != "page":
                return PlainTextResponse(content="Not Found", status_code=404)

            for entry in payload.entry:
                for event in entry.messaging:
                    self._process_event(event)

            return PlainTextResponse(content="EVENT_RECEIVED")

    def _process_event(self, event: WebhookEvent) -> None:
        if event.postback or (event.message and event.message.quick_reply):
            self._postback_registry.handle_event(event)
        elif event.message:
            self._message_registry.handle_event(event)

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:  # noqa: S104
        import uvicorn

        uvicorn.run(self.app, host=host, port=port)
