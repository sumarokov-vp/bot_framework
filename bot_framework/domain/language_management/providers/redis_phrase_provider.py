import redis

from bot_framework.domain.language_management.providers.protocols import IPhraseProvider


class RedisPhraseProvider(IPhraseProvider):
    def __init__(self, redis_url: str) -> None:
        self._redis = redis.from_url(redis_url)

    def _get_key(self, key: str, language_code: str) -> str:
        return f"phrase:{key}:{language_code}"

    def _get_default_language(self) -> str:
        value = self._redis.get("languages:default")
        if value is None:
            return "en"
        if isinstance(value, bytes):
            return value.decode()
        return str(value)

    def _get_value(self, redis_key: str) -> str | None:
        value = self._redis.get(redis_key)
        if value is None:
            return None
        if isinstance(value, bytes):
            return value.decode()
        return str(value)

    def get_phrase(self, key: str, language_code: str) -> str:
        redis_key = self._get_key(key, language_code)
        value = self._get_value(redis_key)
        if value is not None:
            return value

        default_lang = self._get_default_language()
        if language_code != default_lang:
            fallback_key = self._get_key(key, default_lang)
            value = self._get_value(fallback_key)
            if value is not None:
                return value

        return f"[Missing phrase: {key}]"
