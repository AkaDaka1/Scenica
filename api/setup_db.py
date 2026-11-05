"""Создание структуры БД из ``migrations/struct.sql``.

Запуск::

    python -m api.setup_db

Параметры подключения берутся из ``api/config.py`` (переменные окружения
или ``.env`` в корне проекта). Секреты в этом файле не хранятся.
"""
from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

_ROOT_DIR = Path(__file__).resolve().parents[1]
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from api.config import DATABASE_URL  # noqa: E402

_SQL_FILE = _ROOT_DIR / "migrations" / "struct.sql"


def execute_sql_from_file(file_path: str | Path) -> None:
    """Выполняет SQL-команды из файла, разделённые точкой с запятой."""
    engine = create_engine(DATABASE_URL)
    sql_commands = Path(file_path).read_text(encoding="utf-8")

    with engine.connect() as conn:
        for statement in sql_commands.split(";"):
            statement = statement.strip()
            if not statement:
                continue
            try:
                conn.execute(text(statement))
                conn.commit()
                print(f"Выполнена команда: {statement[:50]}...")
            except ProgrammingError as exc:
                print(f"Ошибка выполнения команды: {exc}")
                conn.rollback()
            except Exception as exc:  # noqa: BLE001 - CLI-скрипт печатает причину
                print(f"Неизвестная ошибка: {exc}")
                conn.rollback()


def setup_database() -> None:
    """Создаёт структуру базы данных из ``migrations/struct.sql``."""
    print("Начинаем настройку базы данных...")
    execute_sql_from_file(_SQL_FILE)
    print("Настройка базы данных завершена!")


if __name__ == "__main__":
    setup_database()
