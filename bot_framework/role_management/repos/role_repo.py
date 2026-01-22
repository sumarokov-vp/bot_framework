import psycopg
from psycopg.rows import class_row

from bot_framework.entities.role import Role
from bot_framework.role_management.repos.protocols.i_role_repo import IRoleRepo


class RoleRepo(IRoleRepo):
    def __init__(
        self,
        database_url: str,
    ):
        self.database_url = database_url

    def get_all(self) -> list[Role]:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(Role)) as cur:
                cur.execute(
                    "SELECT * FROM roles WHERE is_active = TRUE ORDER BY name",
                )
                return cur.fetchall()

    def find_by_id(
        self,
        id: int,
    ) -> Role | None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(Role)) as cur:
                cur.execute(
                    "SELECT * FROM roles WHERE id = %(role_id)s AND is_active = TRUE",
                    {
                        "role_id": id,
                    },
                )
                return cur.fetchone()

    def get_by_id(
        self,
        id: int,
    ) -> Role:
        role = self.find_by_id(id)
        if not role:
            raise ValueError(f"Role with id {id} not found")
        return role

    def get_user_roles(
        self,
        user_id: int,
    ) -> list[Role]:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor(row_factory=class_row(Role)) as cur:
                cur.execute(
                    """
                    SELECT r.*
                    FROM user_roles ur
                    JOIN roles r ON ur.role_id = r.id
                    WHERE ur.user_id = %(user_id)s AND r.is_active = TRUE
                    """,
                    {
                        "user_id": user_id,
                    },
                )
                return cur.fetchall()

    def assign_role(
        self,
        user_id: int,
        role_id: int,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%(user_id)s, %(role_id)s)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                    """,
                    {
                        "user_id": user_id,
                        "role_id": role_id,
                    },
                )

    def assign_role_by_name(
        self,
        user_id: int,
        role_name: str,
    ) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_roles (user_id, role_id)
                    SELECT %(user_id)s, r.id
                    FROM roles r
                    WHERE r.name = %(role_name)s AND r.is_active = TRUE
                    ON CONFLICT (user_id, role_id) DO NOTHING
                    """,
                    {
                        "user_id": user_id,
                        "role_name": role_name,
                    },
                )
