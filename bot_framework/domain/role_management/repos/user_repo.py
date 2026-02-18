from datetime import datetime

import psycopg
from psycopg.rows import class_row

from bot_framework.core.entities.user import User
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class UserRepo(IUserRepo):
    def __init__(
        self,
        database_url: str,
    ):
        self.database_url = database_url

    def find_by_id(
        self,
        id: int,
    ) -> User | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    "SELECT * FROM users WHERE id = %(user_id)s",
                    {
                        "user_id": id,
                    },
                )
                return cur.fetchone()

    def get_by_id(
        self,
        id: int,
    ) -> User:
        user = self.find_by_id(id)
        if not user:
            raise ValueError(f"User with id {id} not found")
        return user

    def get_by_name(
        self,
        name: str,
    ) -> list[User]:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    "SELECT * FROM users WHERE username = %(name)s",
                    {
                        "name": name,
                    },
                )
                return cur.fetchall()

    def get_by_role_name(
        self,
        role_name: str,
    ) -> list[User]:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    """
                    SELECT u.*
                    FROM users u
                    JOIN user_roles ur ON u.id = ur.user_id
                    JOIN roles r ON ur.role_id = r.id
                    WHERE r.name = %(role_name)s AND r.is_active = TRUE
                    ORDER BY u.first_name, u.username
                    """,
                    {
                        "role_name": role_name,
                    },
                )
                return cur.fetchall()

    def create(
        self,
        entity: User,
    ) -> User:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    """
                    INSERT INTO users (
                        id,
                        username,
                        first_name,
                        last_name,
                        language_code,
                        is_bot,
                        is_premium,
                        phone_number,
                        party_id
                    )
                    VALUES (
                        %(id)s,
                        %(username)s,
                        %(first_name)s,
                        %(last_name)s,
                        %(language_code)s,
                        %(is_bot)s,
                        %(is_premium)s,
                        %(phone_number)s,
                        %(party_id)s
                    )
                    RETURNING *
                    """,
                    entity.model_dump(),
                )
                user = cur.fetchone()
                if not user:
                    raise ValueError(f"User with id {entity.id} already exists")
                return user

    def update(
        self,
        entity: User,
    ) -> User:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    """
                    UPDATE users SET
                        username = %(username)s,
                        first_name = %(first_name)s,
                        last_name = %(last_name)s,
                        language_code = %(language_code)s,
                        is_bot = %(is_bot)s,
                        is_premium = %(is_premium)s,
                        phone_number = %(phone_number)s,
                        party_id = %(party_id)s,
                        updated_at = NOW()
                    WHERE id = %(id)s
                    RETURNING *
                    """,
                    entity.model_dump(),
                )
                user = cur.fetchone()
                if not user:
                    raise ValueError(f"User with id {entity.id} not found")
                return user

    def delete(
        self,
        entity: User,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM users WHERE id = %(user_id)s",
                    {
                        "user_id": entity.id,
                    },
                )

    def update_last_rejection_at(
        self,
        user_id: int,
        timestamp: datetime,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET last_rejection_at = %(timestamp)s
                    WHERE id = %(user_id)s
                    """,
                    {
                        "user_id": user_id,
                        "timestamp": timestamp,
                    },
                )

    def update_language(
        self,
        user_id: int,
        language_code: str,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET language_code = %(language_code)s
                    WHERE id = %(user_id)s
                    """,
                    {
                        "user_id": user_id,
                        "language_code": language_code,
                    },
                )

    def set_phone_number(
        self,
        user_id: int,
        phone_number: str,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET phone_number = %(phone_number)s
                    WHERE id = %(user_id)s
                    """,
                    {
                        "user_id": user_id,
                        "phone_number": phone_number,
                    },
                )
