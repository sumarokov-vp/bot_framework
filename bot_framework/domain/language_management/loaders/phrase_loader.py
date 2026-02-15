import json
from pathlib import Path

import redis


class PhraseLoader:
    def __init__(self, redis_url: str) -> None:
        self._redis = redis.from_url(redis_url)

    def _get_key(self, phrase_key: str, language_code: str) -> str:
        return f"phrase:{phrase_key}:{language_code}"

    def load_from_json(self, json_path: Path) -> int:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for phrase_key, translations in data.items():
            for language_code, text in translations.items():
                redis_key = self._get_key(phrase_key, language_code)
                self._redis.set(redis_key, text)
                count += 1
        return count
