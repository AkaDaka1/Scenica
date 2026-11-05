"""
Тесты для конфигурационных файлов.

Тесты не зависят от наличия локального ``.env``: секреты подставляются
через переменные окружения и ``importlib.reload``.
"""
import importlib
import os
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]

_MANDATORY_VARS = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "API_BASE_URL",
]


@pytest.fixture
def isolated_env(monkeypatch):
    """Изолирует конфиг от реального ``.env`` и переменных окружения."""
    for key in _MANDATORY_VARS + ["API_BASE_URL"]:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    # load_dotenv не должен перетирать подставленные значения
    monkeypatch.setattr("dotenv.load_dotenv", lambda *args, **kwargs: False)
    yield monkeypatch


class TestApiConfig:
    """Тесты для конфигурации API."""

    def test_api_config_defaults(self, isolated_env):
        import api.config

        config = importlib.reload(api.config)

        assert config.DB_PORT == "5432"
        assert config.ALGORITHM == "HS256"
        assert config.ACCESS_TOKEN_EXPIRE_MINUTES == 30

    def test_api_config_database_url_format(self, isolated_env):
        import api.config

        config = importlib.reload(api.config)

        assert config.DATABASE_URL.startswith("postgresql+psycopg://")
        assert "localhost" in config.DATABASE_URL
        assert "5432" in config.DATABASE_URL

    def test_api_config_requires_secret_key(self, isolated_env):
        isolated_env.delenv("SECRET_KEY", raising=False)
        import api.config

        with pytest.raises(RuntimeError, match="SECRET_KEY"):
            importlib.reload(api.config)

    def test_api_config_secret_key_from_env(self, isolated_env):
        isolated_env.setenv("SECRET_KEY", "another-test-key")
        import api.config

        config = importlib.reload(api.config)

        assert config.SECRET_KEY == "another-test-key"

    def test_n8n_webhook_optional(self, isolated_env):
        import api.config

        config = importlib.reload(api.config)

        assert config.N8N_TZ_WEBHOOK_URL == ""
        assert config.N8N_TZ_TIMEOUT_SEC == 120


class TestAppConfig:
    """Тесты для конфигурации десктопного клиента."""

    def test_app_config_api_base_url_default(self, isolated_env):
        import app.config

        config = importlib.reload(app.config)

        assert config.API_BASE_URL == "http://localhost:8000"

    def test_app_config_api_base_url_from_env(self, isolated_env):
        isolated_env.setenv("API_BASE_URL", "http://custom-api:9000/")
        import app.config

        config = importlib.reload(app.config)

        # Завершающий слэш нормализуется при импорте
        assert config.API_BASE_URL == "http://custom-api:9000"


class TestEnvExample:
    """Тесты для шаблона окружения ``.env.example``."""

    def test_env_example_exists(self):
        assert (_ROOT / ".env.example").is_file()

    def test_env_example_contains_required_vars(self):
        content = (_ROOT / ".env.example").read_text(encoding="utf-8")
        for var in _MANDATORY_VARS:
            assert var in content, f"Required variable {var} not found in .env.example"

    def test_env_example_has_no_real_secrets(self):
        content = (_ROOT / ".env.example").read_text(encoding="utf-8")
        assert "change-me" in content
        assert "SECRET_KEY=change-me" in content

