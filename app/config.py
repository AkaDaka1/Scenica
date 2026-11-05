"""
Конфигурация десктопного клиента Scenica.

Клиент не подключается к базе данных напрямую: единственный обязательный
параметр — адрес API. Секреты здесь не нужны.
"""
import os

from dotenv import load_dotenv

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_PATH = os.path.join(_ROOT_DIR, ".env")

if os.path.exists(_ENV_PATH):
    load_dotenv(_ENV_PATH, override=False)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
