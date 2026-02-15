import json
from pathlib import Path

import psycopg


class RoleLoader:
    def __init__(self, database_url: str) -> None:
        self._database_url = database_url

    def load_from_json(self, json_path: Path) -> int:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        roles = data.get("roles", [])
        if not roles:
            return 0

        with psycopg.connect(self._database_url) as conn:
            with conn.cursor() as cur:
                for role in roles:
                    cur.execute(
                        """
                        INSERT INTO roles (name, description)
                        VALUES (%(name)s, %(description)s)
                        ON CONFLICT (name) DO NOTHING
                        """,
                        {
                            "name": role["name"],
                            "description": role.get("description", ""),
                        },
                    )
            conn.commit()
        return len(roles)
