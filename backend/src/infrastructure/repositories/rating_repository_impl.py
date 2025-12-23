from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from src.domain.repositories.rating_repository import RatingRepository
from src.infrastructure.database.models import PostRating


class RatingRepositoryImpl(RatingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_post_rating(self, post_id: str) -> int:
        try:
            post_uuid = UUID(post_id)
        except ValueError:
            return 0

        result = await self.session.execute(
            select(func.coalesce(func.sum(PostRating.value), 0)).where(
                PostRating.post_id == post_uuid
            )
        )
        return result.scalar() or 0

    async def get_user_rating(self, user_id: str, post_id: str) -> int | None:
        try:
            user_uuid = UUID(user_id)
            post_uuid = UUID(post_id)
        except ValueError:
            return None

        result = await self.session.execute(
            select(PostRating).where(
                PostRating.user_id == user_uuid, PostRating.post_id == post_uuid
            )
        )
        rating = result.scalar_one_or_none()
        return rating.value if rating else None

    async def set_rating(self, user_id: str, post_id: str, value: int) -> bool:
        try:
            user_uuid = UUID(user_id)
            post_uuid = UUID(post_id)
        except ValueError:
            return False

        result = await self.session.execute(
            select(PostRating).where(
                PostRating.user_id == user_uuid, PostRating.post_id == post_uuid
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.value = value
            self.session.add(existing)
        else:
            rating = PostRating(user_id=user_uuid, post_id=post_uuid, value=value)
            self.session.add(rating)

        await self.session.commit()
        return True

    async def remove_rating(self, user_id: str, post_id: str) -> bool:
        try:
            user_uuid = UUID(user_id)
            post_uuid = UUID(post_id)
        except ValueError:
            return False

        result = await self.session.execute(
            select(PostRating).where(
                PostRating.user_id == user_uuid, PostRating.post_id == post_uuid
            )
        )
        rating = result.scalar_one_or_none()

        if rating:
            await self.session.delete(rating)
            await self.session.commit()

        return True
