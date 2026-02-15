import json

import redis

from bot_framework.features.flows.request_role_flow.entities import RequestRoleFlowState


class RedisRequestRoleFlowStateStorage:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)  # pyright: ignore[reportUnknownMemberType]
        self.ttl = 600

    def _get_key(self, telegram_id: int) -> str:
        return f"request_role_flow:{telegram_id}"

    def save_selected_role(self, telegram_id: int, role_id: int) -> None:
        key = self._get_key(telegram_id)
        state = RequestRoleFlowState(
            requester_user_id=telegram_id,
            selected_role_id=role_id,
        )
        self.redis_client.set(key, state.model_dump_json(), ex=self.ttl)

    def get_state(self, telegram_id: int) -> RequestRoleFlowState | None:
        key = self._get_key(telegram_id)
        data = self.redis_client.get(key)
        if not data:
            return None
        return RequestRoleFlowState.model_validate(json.loads(data))  # pyright: ignore[reportArgumentType]

    def clear_state(self, telegram_id: int) -> None:
        key = self._get_key(telegram_id)
        self.redis_client.delete(key)
