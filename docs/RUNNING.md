# Запуск и переменные окружения

## Установка зависимостей

Нужен Python 3.11+. Рекомендуется отдельное виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

## Окружение

В репозитории нет реальных секретов: создайте `.env` из шаблона и заполните
значения.

```bash
cp .env.example .env
```

`SECRET_KEY` обязателен — без него API не запустится. Сгенерируйте значение:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

| Переменная | Назначение | Значение по умолчанию |
|------------|------------|-----------------------|
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Подключение к PostgreSQL | `localhost`, `5432`, `theater`, `postgres`, `postgres` |
| `SECRET_KEY` | Подпись JWT, обязательна | — |
| `ALGORITHM` | Алгоритм подписи JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена | `30` |
| `API_BASE_URL` | Адрес API для десктопного клиента | `http://localhost:8000` |
| `SCENARIO_TZ_UPLOAD_ROOT` | Каталог хранения загруженных ТЗ | `data/scenario_tz` под корнем проекта |
| `N8N_TZ_WEBHOOK_URL` | URL POST-вебхука n8n для `POST .../tz-spec/process`. Пусто — обработка отключена (ответ 400 с пояснением) | — |
| `N8N_TZ_TIMEOUT_SEC` | Таймаут HTTP к n8n в секундах | `120` |

Секреты попадают в контейнеры только через переменные окружения; `.env`
исключён из Docker-контекста через `.dockerignore`.

## Настройка базы данных

Вариант с Docker (PostgreSQL вместе с API):

```bash
docker compose up --build
```

Локальная установка:

1. Убедитесь, что PostgreSQL запущен и параметры из `.env` верны.
2. Создайте структуру базы:

```bash
python -m api.setup_db
```

3. Если база существовала **до** добавления полей ТЗ для сценариев, один раз
   примените миграцию колонок:

```bash
python scripts/apply_scenario_tz_migration.py
```

(Или выполните SQL из `migrations/add_scenario_tz_columns.sql` вручную.)

## Запуск API

### Вариант 1: через uvicorn

```bash
uvicorn api.api:app --reload --host 127.0.0.1 --port 8000
```

### Вариант 2: через Python

```bash
python start_api.py
```

API доступен по адресу http://localhost:8000, документация —
http://localhost:8000/docs.

## Тестирование

Тесты API и CRUD работают на SQLite в памяти и не требуют запущенной
PostgreSQL:

```bash
python -m pytest
```

Отдельный модуль:

```bash
pytest tests/test_api.py
```

## Запуск клиента

После запуска API:

```bash
python start_app.py
```
