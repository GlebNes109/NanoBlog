from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from src.domain.models.posts import PostRead
from src.domain.repositories.favorite_repository import FavoriteRepository
from src.infrastructure.database.models import Favorite, Post, User, PostRating, Comment


class FavoriteRepositoryImpl(FavoriteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_favorites(self, user_id: str) -> list[PostRead]:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return []
        
        statement = (
            select(Post, User, func.coalesce(func.sum(PostRating.value), 0).label("rating"),
                   func.count(Comment.id.distinct()).label("comments_count"))
            .join(Favorite, Favorite.post_id == Post.id)
            .join(User, Post.author_id == User.id)
            .outerjoin(PostRating, PostRating.post_id == Post.id)
            .outerjoin(Comment, Comment.post_id == Post.id)
            .where(Favorite.user_id == user_uuid)
            .group_by(Post.id, User.id)
            .order_by(Post.created_at.desc())
        )
        
        result = await self.session.execute(statement)
        rows = result.all()
        
        return [
            PostRead(
                id=str(post.id),
                authorId=str(post.author_id),
                authorLogin=user.login,
                authorAvatar=user.avatar_url,
                title=post.title,
                content=post.content,
                image_url=post.image_url,
                rating=rating or 0,
                user_rating=None,
                comments_count=comments_count or 0,
                is_favorited=True,
                createdAt=post.created_at,
                updatedAt=post.updated_at,
            )
            for post, user, rating, comments_count in rows
        ]

    async def add(self, user_id: str, post_id: str) -> bool:
        try:
            user_uuid = UUID(user_id)
            post_uuid = UUID(post_id)
        except ValueError:
            return False
        
        existing = await self.session.execute(
            select(Favorite).where(Favorite.user_id == user_uuid, Favorite.post_id == post_uuid)
        )
        if existing.scalar_one_or_none():
            return False
        
        favorite = Favorite(user_id=user_uuid, post_id=post_uuid)
        self.session.add(favorite)
        await self.session.commit()
        return True

    async def remove(self, user_id: str, post_id: str) -> bool:
        try:
            user_uuid = UUID(user_id)
            post_uuid = UUID(post_id)
        except ValueError:
            return False
        
        result = await self.session.execute(
            select(Favorite).where(Favorite.user_id == user_uuid, Favorite.post_id == post_uuid)
        )
        favorite = result.scalar_one_or_none()
        
        if not favorite:
            return False
        
        await self.session.delete(favorite)
        await self.session.commit()
        return True

    async def is_favorited(self, user_id: str, post_id: str) -> bool:
        try:
            user_uuid = UUID(user_id)
            post_uuid = UUID(post_id)
        except ValueError:
            return False
        
        result = await self.session.execute(
            select(Favorite).where(Favorite.user_id == user_uuid, Favorite.post_id == post_uuid)
        )
        return result.scalar_one_or_none() is not None


