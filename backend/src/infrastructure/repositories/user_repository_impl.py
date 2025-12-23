from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import or_, select

from src.domain.models.users import UserCreate, UserProfileUpdate, UserPublic, UserRead
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models import User as UserORM


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> UserRead | None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None
        user = await self.session.get(UserORM, user_uuid)
        return self._to_read(user) if user else None

    async def get_by_login(self, login: str) -> UserRead | None:
        statement = select(UserORM).where(UserORM.login == login)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return self._to_read(user) if user else None

    async def get_by_email(self, email: str) -> UserRead | None:
        statement = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return self._to_read(user) if user else None

    async def create(self, user: UserCreate) -> UserRead:
        user_orm = UserORM(
            id=uuid4(),
            email=user.email,
            login=user.login,
            password_hash=user.password,
            created_at=user.createdAt,
            updated_at=user.updatedAt,
        )
        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        return self._to_read(user_orm)

    async def update_profile(self, user_id: str, profile: UserProfileUpdate) -> UserPublic | None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None

        user = await self.session.get(UserORM, user_uuid)
        if not user:
            return None

        if profile.email is not None:
            user.email = profile.email
        if profile.login is not None:
            user.login = profile.login
        if profile.bio is not None:
            user.bio = profile.bio
        user.updated_at = datetime.utcnow()

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return self._to_public(user)

    async def update_avatar(self, user_id: str, avatar_url: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False

        user = await self.session.get(UserORM, user_uuid)
        if not user:
            return False

        user.avatar_url = avatar_url
        user.updated_at = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()
        return True

    async def delete(self, user_id: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False

        user = await self.session.get(UserORM, user_uuid)
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True

    async def search(self, query: str) -> list[UserPublic]:
        search_term = f"%{query}%"
        statement = (
            select(UserORM)
            .where(or_(UserORM.login.ilike(search_term), UserORM.email.ilike(search_term)))
            .order_by(UserORM.login)
        )

        result = await self.session.execute(statement)
        users = result.scalars().all()
        return [self._to_public(user) for user in users]

    async def get_public_profile(self, user_id: str) -> UserPublic | None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None

        user = await self.session.get(UserORM, user_uuid)
        return self._to_public(user) if user else None

    @staticmethod
    def _to_read(user: UserORM) -> UserRead:
        return UserRead(
            id=str(user.id),
            email=user.email,
            login=user.login,
            password=user.password_hash,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
        )

    @staticmethod
    def _to_public(user: UserORM) -> UserPublic:
        return UserPublic(
            id=str(user.id),
            email=user.email,
            login=user.login,
            avatar_url=user.avatar_url,
            bio=user.bio,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
        )
