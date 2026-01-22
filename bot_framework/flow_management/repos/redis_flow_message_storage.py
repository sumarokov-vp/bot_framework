from __future__ import annotations

import redis


class RedisFlowMessageStorage:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)  # pyright: ignore[reportUnknownMemberType]
        self.ttl = 600

    def _get_key(self, telegram_id: int, flow_name: str) -> str:
        return f"flow_messages:{telegram_id}:{flow_name}"

    def _get_pattern(self, telegram_id: int) -> str:
        return f"flow_messages:{telegram_id}:*"

    def add_message(self, telegram_id: int, flow_name: str, message_id: int) -> None:
        key = self._get_key(telegram_id, flow_name)
        self.redis_client.rpush(key, message_id)
        self.redis_client.expire(key, self.ttl)

    def get_messages(self, telegram_id: int, flow_name: str) -> list[int]:
        key = self._get_key(telegram_id, flow_name)
        messages = self.redis_client.lrange(key, 0, -1)
        return [int(m) for m in messages]  # pyright: ignore[reportGeneralTypeIssues]

    def clear_messages(self, telegram_id: int, flow_name: str) -> None:
        key = self._get_key(telegram_id, flow_name)
        self.redis_client.delete(key)

    def clear_all_messages(self, telegram_id: int) -> None:
        pattern = self._get_pattern(telegram_id)
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)  # pyright: ignore[reportGeneralTypeIssues]
