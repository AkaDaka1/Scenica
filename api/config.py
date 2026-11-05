"""
Конфигурация API-слоя Scenica.

Все значения читаются из переменных окружения или из файла ``.env``
в корне проекта. Секреты в исходном коде не хранятся: ``SECRET_KEY``
обязателен и должен быть задан до запуска API.
"""
import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_PATH = os.path.join(_ROOT_DIR, ".env")

# .env нужен только для локальной разработки. Реальные переменные окружения
# имеют приоритет и не перезаписываются файлом.
if os.path.exists(_ENV_PATH):
    load_dotenv(_ENV_PATH, override=False)
    logger.info("Loaded .env from: %s", _ENV_PATH)
else:
    logger.warning(".env not found at: %s", _ENV_PATH)

# --- База данных ---------------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "theater")
DB_USER = os.getenv("DB_USER", "postgres")
# Пароль по умолчанию подходит только для локального docker-compose.
# В любом другом окружении задайте DB_PASSWORD явно.
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# --- JWT -----------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Copy .env.example to .env and set a strong "
        "random value (for example: openssl rand -hex 32)."
    )
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# SQLAlchemy URL. psycopg v3 используется как драйвер PostgreSQL.
DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- Клиент --------------------------------------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

# --- Файлы ТЗ сценариев --------------------------------------------------
_DEFAULT_TZ_DIR = os.path.join(_ROOT_DIR, "data", "scenario_tz")
SCENARIO_TZ_UPLOAD_ROOT = (
    os.getenv("SCENARIO_TZ_UPLOAD_ROOT", "").strip() or _DEFAULT_TZ_DIR
)

# n8n: POST-вебхук для обработки ТЗ сценария. Пустое значение отключает
# интеграцию; API вернёт понятную ошибку 400.
N8N_TZ_WEBHOOK_URL = os.getenv("N8N_TZ_WEBHOOK_URL", "").strip()
N8N_TZ_TIMEOUT_SEC = int(os.getenv("N8N_TZ_TIMEOUT_SEC", "120"))
