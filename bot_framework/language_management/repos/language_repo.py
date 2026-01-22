import psycopg
from psycopg.rows import class_row

from bot_framework.language_management.entities.language import Language
from bot_framework.language_management.repos.protocols.i_language_repo import ILanguageRepo


class LanguageRepo(ILanguageRepo):
    def __init__(
        self,
        database_url: str,
    ):
        self.database_url = database_url

    def get_all(self) -> list[Language]:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(Language)) as cur:
                cur.execute(
                    "SELECT * FROM languages WHERE is_active = TRUE ORDER BY code",
                )
                return cur.fetchall()

    def get_by_key(
        self,
        key: str,
    ) -> Language:
        language = self.find_by_key(key)
        if not language:
            raise ValueError(f"Language with code {key} not found")
        return language

    def find_by_key(
        self,
        key: str,
    ) -> Language | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(Language)) as cur:
                cur.execute(
                    "SELECT * FROM languages WHERE code = %(key)s",
                    {
                        "key": key,
                    },
                )
                return cur.fetchone()

    def get_by_id(
        self,
        id: int,
    ) -> Language:
        language = self.find_by_id(id)
        if not language:
            raise ValueError(f"Language with id {id} not found")
        return language

    def find_by_id(
        self,
        id: int,
    ) -> Language | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(Language)) as cur:
                cur.execute(
                    "SELECT * FROM languages WHERE code = %(id)s",
                    {
                        "id": id,
                    },
                )
                return cur.fetchone()
