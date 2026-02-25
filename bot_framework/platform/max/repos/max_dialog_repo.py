import psycopg


class MaxDialogRepo:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def upsert(self, user_id: int, chat_id: int) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO max_dialogs (user_id, chat_id)
                    VALUES (%(user_id)s, %(chat_id)s)
                    ON CONFLICT (user_id) DO UPDATE SET chat_id = EXCLUDED.chat_id
                    """,
                    {
                        "user_id": user_id,
                        "chat_id": chat_id,
                    },
                )

    def get_chat_id(self, user_id: int) -> int | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT chat_id FROM max_dialogs WHERE user_id = %(user_id)s",
                    {
                        "user_id": user_id,
                    },
                )
                row = cur.fetchone()
                return row[0] if row else None
