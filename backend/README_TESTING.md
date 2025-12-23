# Запуск тестов бэкенда

## Решение проблемы с импортами

Проблема `ModuleNotFoundError: No module named 'src'` была исправлена добавлением `pythonpath = .` в `pytest.ini` и `pyproject.toml`.

## О папке microblog.egg-info

Папка `microblog.egg-info` создается автоматически при установке пакета через:
- `pip install -e .` (editable install)
- `pip install .`

Эта папка содержит метаданные установленного пакета и может быть удалена. Она добавлена в `.gitignore`, чтобы не попадала в репозиторий.

Если она появилась в неправильном месте (например, в `src/`), удалите её:
```bash
rm -rf src/microblog.egg-info
# или
find . -name "*.egg-info" -type d -exec rm -rf {} +
```

## Установка зависимостей

```bash
cd backend
pip install -e ".[dev]"
```

Или если используете requirements.txt:
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx faker
```

## Запуск тестов

```bash
# Все тесты
pytest

# Только unit тесты
pytest tests/unit

# Только интеграционные тесты
pytest tests/integration

# С coverage отчетом
pytest --cov=src --cov-report=html
# Отчет будет в htmlcov/index.html
```

## Проверка, что проблема решена

Если тесты запускаются без ошибок импорта, значит проблема решена.

Если все еще есть проблемы:
1. Убедитесь, что вы находитесь в директории `backend/`
2. Проверьте, что `pythonpath = .` есть в `pytest.ini`
3. Установите зависимости: `pip install -e ".[dev]"`

