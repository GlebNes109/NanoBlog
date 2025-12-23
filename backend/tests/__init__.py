"""Tests package - устанавливаем переменные окружения до импорта модулей."""
import os

# Устанавливаем переменные окружения ДО импорта любых модулей
# Это гарантирует, что settings.py сможет их прочитать при загрузке
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SERVER_ADDRESS", "0.0.0.0:8000")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
