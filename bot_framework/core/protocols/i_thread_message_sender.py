from typing import Any, Protocol


class IThreadMessageSender(Protocol):
    def send_message(
        self,
        chat_id: int | str,
        text: str,
        parse_mode: str | None = None,
        entities: Any | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        reply_to_message_id: int | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_markup: Any | None = None,
        timeout: int | None = None,
        message_thread_id: int | None = None,
        reply_parameters: Any | None = None,
        link_preview_options: Any | None = None,
        business_connection_id: str | None = None,
        message_effect_id: str | None = None,
    ) -> Any: ...
