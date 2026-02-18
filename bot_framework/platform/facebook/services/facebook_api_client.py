from __future__ import annotations

from typing import Any

import httpx

GRAPH_API_BASE_URL = "https://graph.facebook.com/v21.0"


class FacebookApiClient:
    def __init__(self, page_access_token: str) -> None:
        self._token = page_access_token
        self._client = httpx.Client(
            base_url=GRAPH_API_BASE_URL,
            headers={"Authorization": f"Bearer {page_access_token}"},
            timeout=30.0,
        )

    def send_message(self, recipient_id: str, message_payload: dict[str, Any]) -> dict[str, Any]:
        response = self._client.post(
            "/me/messages",
            json={
                "recipient": {"id": recipient_id},
                "message": message_payload,
                "messaging_type": "RESPONSE",
            },
        )
        response.raise_for_status()
        return response.json()

    def send_attachment(self, recipient_id: str, attachment_type: str, url: str) -> dict[str, Any]:
        response = self._client.post(
            "/me/messages",
            json={
                "recipient": {"id": recipient_id},
                "message": {
                    "attachment": {
                        "type": attachment_type,
                        "payload": {"url": url, "is_reusable": True},
                    }
                },
                "messaging_type": "RESPONSE",
            },
        )
        response.raise_for_status()
        return response.json()

    def get_user_profile(self, psid: str) -> dict[str, Any]:
        response = self._client.get(
            f"/{psid}",
            params={"fields": "first_name,last_name,locale"},
        )
        response.raise_for_status()
        return response.json()

    def delete_message(self, message_id: str) -> None:
        response = self._client.delete(f"/{message_id}")
        response.raise_for_status()

    def close(self) -> None:
        self._client.close()
