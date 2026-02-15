from __future__ import annotations

import json

import redis

from bot_framework.domain.flow_management.entities import FlowStackEntry


class RedisFlowStackStorage:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
        self.ttl = 600

    def _get_key(self, telegram_id: int) -> str:
        return f"flow_stack:{telegram_id}"

    def _get_raw_stack(self, telegram_id: int) -> list[dict]:
        value = self.redis_client.get(self._get_key(telegram_id))
        if value is None:
            return []
        if isinstance(value, bytes):
            return json.loads(value.decode())
        if isinstance(value, str):
            return json.loads(value)
        return []

    def _save_raw_stack(self, telegram_id: int, stack: list[dict]) -> None:
        self.redis_client.setex(
            name=self._get_key(telegram_id),
            time=self.ttl,
            value=json.dumps(stack),
        )

    def push(self, telegram_id: int, entry: FlowStackEntry) -> None:
        stack = self._get_raw_stack(telegram_id)
        stack.append(entry.model_dump(mode="json"))
        self._save_raw_stack(telegram_id, stack)

    def pop(self, telegram_id: int) -> FlowStackEntry | None:
        stack = self._get_raw_stack(telegram_id)
        if not stack:
            return None
        entry_dict = stack.pop()
        self._save_raw_stack(telegram_id, stack)
        return FlowStackEntry.model_validate(entry_dict)

    def get_stack(self, telegram_id: int) -> list[FlowStackEntry]:
        raw_stack = self._get_raw_stack(telegram_id)
        return [FlowStackEntry.model_validate(entry) for entry in raw_stack]

    def clear(self, telegram_id: int) -> None:
        self.redis_client.delete(self._get_key(telegram_id))
