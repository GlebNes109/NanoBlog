"""Pytest configuration for integration tests."""
import os
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Переменные окружения уже установлены в tests/__init__.py и tests/conftest.py
# Переопределяем DATABASE_URL для интеграционных тестов (используем PostgreSQL)
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_microblog")

from src.main import app
from src.infrastructure.database.database import get_session
from src.infrastructure.database.models import User as UserORM
from src.infrastructure.password_hasher_impl import sha256HashCreator
from uuid import uuid4


# Test database URL
TEST_DATABASE_URL = os.environ.get("DATABASE_URL")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    try:
        # Test connection
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception:
        await engine.dispose()
        pytest.skip("Database not available")
    
    yield engine
    
    # Drop all tables after tests
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
    except Exception:
        pass
    
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create test database session."""
    async_session_maker = async_sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(test_session):
    """Create test client with test database session."""
    async def override_get_session():
        yield test_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session):
    """Create a test user."""
    hasher = sha256HashCreator()
    password_hash = await hasher.hash("testpassword")
    
    user = UserORM(
        id=uuid4(),
        email="test@example.com",
        login="testuser",
        password_hash=password_hash,
    )
    
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for test user."""
    from src.core.security import create_access_token
    
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
