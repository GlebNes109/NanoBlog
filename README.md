# MicroBlog

Микроблог с JWT авторизацией, CRUD операциями для постов, комментариями, рейтингами и избранным.

## Структура проекта

- `backend/` - FastAPI бэкенд
- `frontend/micro-blog/` - React фронтенд
- `docker-compose.yml` - конфигурация для запуска всех сервисов

### ER-диаграмма

![ER.png](docs/ER.png)

## Запуск проекта

### Требования

- Docker и Docker Compose

### Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd MicroBlog
```

2. Запустите проект через Docker Compose:
```bash
docker-compose up --build
```

Проект будет доступен по адресам:
- Фронтенд: http://localhost:3000
- Бэкенд API: http://localhost:8000
- Swagger документация: http://localhost:8000/docs

3. Остановка:
```bash
docker-compose down
```

### Переменные окружения

Создайте файл `.env` в корне проекта (опционально):

```env
POSTGRES_USER=microblog
POSTGRES_PASSWORD=microblog
POSTGRES_DB=microblog
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://microblog:microblog@postgres:5432/microblog
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

## Тестирование

### Backend тесты

1. Перейдите в директорию backend:
```bash
cd backend
```

2. Установите зависимости:
```bash
pip install -e ".[dev]"
```

3. Запустите тесты:
```bash
# Все тесты
pytest

# Только unit тесты
pytest tests/unit

# Только интеграционные тесты (требует PostgreSQL)
pytest tests/integration

# С coverage отчетом
pytest --cov=src --cov-report=html
# Отчет будет в htmlcov/index.html и в консоли
```

**Примечание:** Интеграционные тесты требуют запущенную базу данных PostgreSQL. Для их пропуска установите переменную окружения:
```bash
SKIP_INTEGRATION_TESTS=true pytest
```

### Frontend тесты

1. Перейдите в директорию frontend:
```bash
cd frontend/micro-blog
```

2. Установите зависимости:
```bash
npm install
```

3. Запустите тесты:
```bash
# Unit и component тесты
npm run test:run

# С coverage отчетом
npm run test:coverage

# E2E тесты
npm run test:e2e

# Все тесты
npm run test:all
```

### Запуск тестов в Docker

Можно также запустить тесты внутри контейнеров:

**Backend:**
```bash
docker-compose exec backend pytest
```

**Frontend:**
```bash
docker-compose exec frontend npm run test:run
```

## Локальная разработка

### Backend

1. Установите зависимости:
```bash
cd backend
pip install -e ".[dev]"
```

2. Создайте `.env` файл с настройками базы данных

3. Запустите только PostgreSQL через Docker:
```bash
docker-compose up postgres -d
```

4. Запустите бэкенд локально:
```bash
cd backend
uvicorn src.main:app --reload
```

### Frontend

1. Установите зависимости:
```bash
cd frontend/micro-blog
npm install
```

2. Запустите dev сервер:
```bash
npm run dev
```
