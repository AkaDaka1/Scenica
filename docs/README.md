# Документация Scenica

- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) — назначение, предметная область и
  ключевые решения.
- [ARCHITECTURE.md](ARCHITECTURE.md) — слои системы, потоки данных, работа с ТЗ
  сценариев.
- [API_DOCS.md](API_DOCS.md) — эндпоинты, схемы запросов и ответов.
- [RUNNING.md](RUNNING.md) — установка зависимостей, настройка БД, переменные
  окружения, запуск.
- [USER_GUIDE.md](USER_GUIDE.md) — работа сотрудника в десктопном клиенте.
- [SECURITY.md](SECURITY.md) — рекомендации по безопасности.
- [SECURITY_ROLES.md](SECURITY_ROLES.md) — роли и права доступа.
- [COMPARISON.md](COMPARISON.md) — сравнение прямого доступа к БД и API-слоя.

## Структура `api/`

- `database.py` — подключение к БД и сессии SQLAlchemy
- `models.py` — ORM-модели SQLAlchemy
- `schemas.py` — Pydantic-схемы
- `crud.py` — операции CRUD
- `auth.py` — JWT-аутентификация
- `rbac.py` — проверка ролей и прав
- `public_api.py` — публичные эндпоинты для мобильного клиента
- `scenario_files.py` — хранение и безопасное разрешение путей файлов ТЗ
- `api.py` — FastAPI-эндпоинты
- `setup_db.py` — создание схемы БД из `migrations/struct.sql`
- `run_api_direct.py` — реэкспорт `app` для совместимости; предпочтительно
  `uvicorn api.api:app`

## Установка и запуск

Полная инструкция — в [RUNNING.md](RUNNING.md). Кратко:

```bash
pip install -r requirements.txt
cp .env.example .env      # заполните SECRET_KEY
python -m api.setup_db
python start_api.py
```

## Эндпоинты

API предоставляет CRUD для всех сущностей системы:

- `/employees/` — сотрудники
- `/franchises/` — франшизы
- `/theaters/` — театры
- `/halls/` — залы
- `/scenarios/` — сценарии; см. также `/scenarios/{id}/tz-spec/*` (файл ТЗ, n8n)
  в [API_DOCS.md](API_DOCS.md)
- `/acts/`, `/parts/` — акты и части сценариев
- `/shows/` — показы
- `/customers/`, `/tickets/` — клиенты и билеты
- `/votes_common/`, `/votes_vip/` — голосования
- `/equipments/`, `/rents_equipment/` — оборудование и аренда оборудования
- `/services/`, `/rents_service/` — услуги и аренда услуг
- `/public/v1/*` — публичный API для мобильного клиента

Защищённые маршруты требуют JWT, получаемый через `POST /token`.

## Безопасность

- Пароли хешируются с использованием bcrypt
- Аутентификация выполняется через JWT-токены
- Данные валидируются Pydantic-схемами
- Секреты задаются только через переменные окружения / `.env`
