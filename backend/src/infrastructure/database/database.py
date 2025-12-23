from collections.abc import AsyncGenerator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel, select

from src.core.settings import settings
from src.infrastructure.database.models import (  # noqa: F401
    Comment,
    Favorite,
    Post,
    PostRating,
    PostTag,
    Subscription,
    Tag,
    User as UserORM,
)

engine = create_async_engine(settings.database_url, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_by_id(session: AsyncSession, user_id: str) -> UserORM | None:
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return None
    return await session.get(UserORM, user_uuid)


async def get_user_by_login(session: AsyncSession, login: str) -> UserORM | None:
    statement = select(UserORM).where(UserORM.login == login)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
