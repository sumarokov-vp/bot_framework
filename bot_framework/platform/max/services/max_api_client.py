from __future__ import annotations

from logging import getLogger
from typing import Any

import httpx

MAX_API_BASE_URL = "https://platform-api.max.ru"
MAX_API_VERSION = "0.1.2"

logger = getLogger(__name__)


class MaxApiClient:
    def __init__(self, token: str) -> None:
        self._token = token
        self._client = httpx.Client(
            base_url=MAX_API_BASE_URL,
            headers={"Authorization": token},
            params={"v": MAX_API_VERSION},
            timeout=35.0,
        )

    def get_me(self) -> dict[str, Any]:
        response = self._client.get("/me")
        response.raise_for_status()
        return response.json()

    def send_message(
        self,
        body: dict[str, Any],
        chat_id: int | None = None,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        if user_id is not None:
            params["user_id"] = user_id
        response = self._client.post("/messages", json=body, params=params)
        if response.is_error:
            logger.error("Max API error %s: %s", response.status_code, response.text)
        response.raise_for_status()
        return response.json()

    def edit_message(self, message_id: str, body: dict[str, Any]) -> dict[str, Any]:
        response = self._client.put(
            "/messages",
            json=body,
            params={"message_id": message_id},
        )
        if response.is_error:
            logger.error("Max API error %s: %s", response.status_code, response.text)
        response.raise_for_status()
        return response.json()

    def delete_message(self, message_id: str) -> dict[str, Any]:
        response = self._client.delete(
            "/messages",
            params={"message_id": message_id},
        )
        if response.is_error:
            logger.error("Max API error %s: %s", response.status_code, response.text)
        response.raise_for_status()
        return response.json()

    def answer_callback(
        self, callback_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        response = self._client.post(
            "/answers",
            json=body if body else {"notification": ""},
            params={"callback_id": callback_id},
        )
        if response.is_error:
            logger.error("Max API error %s: %s", response.status_code, response.text)
        response.raise_for_status()
        return response.json()

    def get_updates(
        self,
        limit: int = 50,
        timeout: int = 30,
        marker: int | None = None,
        types: list[str] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "timeout": timeout}
        if marker is not None:
            params["marker"] = marker
        if types:
            params["types"] = ",".join(types)
        response = self._client.get("/updates", params=params, timeout=timeout + 5.0)
        response.raise_for_status()
        return response.json()

    def get_upload_url(self, upload_type: str) -> dict[str, Any]:
        response = self._client.post(
            "/uploads",
            params={"type": upload_type},
        )
        response.raise_for_status()
        return response.json()

    def upload_file(self, upload_url: str, data: bytes, filename: str) -> dict[str, Any]:
        files = {"file": (filename, data, "application/octet-stream")}
        response = httpx.post(upload_url, files=files, timeout=60.0)
        response.raise_for_status()
        return response.json()

    def download_file(self, url: str) -> bytes:
        response = self._client.get(url)
        response.raise_for_status()
        return response.content

    def close(self) -> None:
        self._client.close()
