import os
import sys

# Корень проекта в PYTHONPATH для импорта backend.*
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Тесты не должны зависеть от локального .env и реальных секретов.
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")
# Тесты используют SQLite в памяти; подключение к PostgreSQL при импорте
# моделей не должно открываться.
os.environ.setdefault("SKIP_DB_STARTUP", "1")
