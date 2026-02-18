import psycopg
from psycopg.rows import class_row

from bot_framework.core.entities.support_topic import SupportTopic


class SupportTopicRepo:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def find_by_user_and_chat(
        self,
        user_id: int,
        chat_id: int,
    ) -> SupportTopic | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(SupportTopic)) as cur:
                cur.execute(
                    """
                    SELECT user_id, chat_id, topic_id
                    FROM support_topics
                    WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s
                    """,
                    {"user_id": user_id, "chat_id": chat_id},
                )
                return cur.fetchone()

    def find_by_chat_and_topic(
        self,
        chat_id: int,
        topic_id: int,
    ) -> SupportTopic | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(SupportTopic)) as cur:
                cur.execute(
                    """
                    SELECT user_id, chat_id, topic_id
                    FROM support_topics
                    WHERE chat_id = %(chat_id)s AND topic_id = %(topic_id)s
                    """,
                    {"chat_id": chat_id, "topic_id": topic_id},
                )
                return cur.fetchone()

    def create(self, entity: SupportTopic) -> SupportTopic:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(SupportTopic)) as cur:
                cur.execute(
                    """
                    INSERT INTO support_topics (user_id, chat_id, topic_id)
                    VALUES (%(user_id)s, %(chat_id)s, %(topic_id)s)
                    RETURNING user_id, chat_id, topic_id
                    """,
                    entity.model_dump(),
                )
                result = cur.fetchone()
                if not result:
                    raise ValueError("Failed to create support topic")
                return result

    def delete_by_user_and_chat(
        self,
        user_id: int,
        chat_id: int,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM support_topics
                    WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s
                    """,
                    {"user_id": user_id, "chat_id": chat_id},
                )
