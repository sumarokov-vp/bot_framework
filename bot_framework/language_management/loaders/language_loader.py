import json
from pathlib import Path

import psycopg
import redis


class LanguageLoader:
    def __init__(self, redis_url: str, database_url: str) -> None:
        self._redis = redis.from_url(redis_url)
        self._database_url = database_url

    def load_from_json(self, json_path: Path) -> None:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        languages = data["languages"]

        # Сохраняем в Redis (для быстрого доступа к default language)
        self._redis.set("languages:list", json.dumps(languages))
        self._redis.set("languages:default", data["default_language"])

        # Синхронизируем с PostgreSQL
        with psycopg.connect(self._database_url) as conn:
            with conn.cursor() as cur:
                for lang in languages:
                    cur.execute(
                        """
                        INSERT INTO languages (code, name, native_name)
                        VALUES (%(code)s, %(name)s, %(native_name)s)
                        ON CONFLICT (code) DO NOTHING
                        """,
                        {
                            "code": lang["code"],
                            "name": lang["name"],
                            "native_name": lang["native_name"],
                        },
                    )
            conn.commit()

    def get_default_language(self) -> str:
        value = self._redis.get("languages:default")
        if value is None:
            return "en"
        if isinstance(value, bytes):
            return value.decode()
        return str(value)
