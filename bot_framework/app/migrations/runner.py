from pathlib import Path

from yoyo import get_backend, read_migrations


def _convert_to_yoyo_url(database_url: str) -> str:
    """Преобразует postgres:// URL в postgresql+psycopg:// для yoyo с psycopg3."""
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def apply_migrations(database_url: str) -> int:
    """
    Применяет миграции bot_framework.
    Возвращает количество применённых миграций.
    """
    migrations_dir = Path(__file__).parent / "sql"
    yoyo_url = _convert_to_yoyo_url(database_url)

    backend = get_backend(yoyo_url)
    migrations = read_migrations(str(migrations_dir))

    with backend.lock():
        to_apply = backend.to_apply(migrations)
        if to_apply:
            backend.apply_migrations(to_apply)
        return len(to_apply)
