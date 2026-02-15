import psycopg

from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import (
    IPhraseRepo,
)


class PhraseRepo(IPhraseRepo):
    def __init__(
        self,
        database_url: str,
    ):
        self.database_url = database_url

    def get_phrase(
        self,
        key: str,
        language_code: str,
    ) -> str:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT text FROM phrases WHERE key = %(key)s"
                    " AND language_code = %(language_code)s",
                    {
                        "key": key,
                        "language_code": language_code,
                    },
                )
                row = cur.fetchone()
                return (
                    str(row[0]) if row else f"[Missing phrase: {key}-{language_code}]"
                )
