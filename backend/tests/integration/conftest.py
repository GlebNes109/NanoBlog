import asyncio
import os
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_microblog"
)

from src.infrastructure.database.database import get_session
from src.infrastructure.database.models import User as UserORM
from src.infrastructure.password_hasher_impl import sha256HashCreator
from src.main import app

TEST_DATABASE_URL = os.environ.get("DATABASE_URL")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception:
        await engine.dispose()
        pytest.skip("Database not available")

    yield engine

    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
    except Exception:
        pass

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    async_session_maker = async_sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(test_session):
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session):
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
    from src.core.security import create_access_token

    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
