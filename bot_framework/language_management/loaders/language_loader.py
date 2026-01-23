import json
from pathlib import Path

import redis


class LanguageLoader:
    def __init__(self, redis_url: str) -> None:
        self._redis = redis.from_url(redis_url)

    def load_from_json(self, json_path: Path) -> None:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        self._redis.set("languages:list", json.dumps(data["languages"]))
        self._redis.set("languages:default", data["default_language"])

    def get_default_language(self) -> str:
        value = self._redis.get("languages:default")
        if value is None:
            return "en"
        if isinstance(value, bytes):
            return value.decode()
        return str(value)
