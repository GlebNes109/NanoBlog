from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func, or_

from src.domain.models.posts import PostCreate, PostRead, PostUpdate
from src.domain.repositories.post_repository import PostRepository
from src.infrastructure.database.models import Post as PostORM, User, PostRating, Favorite, Comment


class PostRepositoryImpl(PostRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, post_id: str, current_user_id: str | None = None) -> PostRead | None:
        try:
            post_uuid = UUID(post_id)
        except ValueError:
            return None

        post = await self.session.get(PostORM, post_uuid)
        if not post:
            return None

        user = await self.session.get(User, post.author_id)
        rating = await self._get_rating(post_uuid)
        comments_count = await self._get_comments_count(post_uuid)

        is_favorited = False
        user_rating = None

        if current_user_id:
            try:
                user_uuid = UUID(current_user_id)
                is_favorited = await self._is_favorited(user_uuid, post_uuid)
                user_rating = await self._get_user_rating(user_uuid, post_uuid)
            except ValueError:
                pass

        return self._to_read(post, user, rating, user_rating, comments_count, is_favorited)

    async def get_all(self, current_user_id: str | None = None) -> list[PostRead]:
        statement = (
            select(
                PostORM,
                User,
                func.coalesce(func.sum(PostRating.value), 0).label("rating"),
                func.count(Comment.id.distinct()).label("comments_count"),
            )
            .join(User, PostORM.author_id == User.id)
            .outerjoin(PostRating, PostRating.post_id == PostORM.id)
            .outerjoin(Comment, Comment.post_id == PostORM.id)
            .group_by(PostORM.id, User.id)
            .order_by(PostORM.created_at.desc())
        )

        result = await self.session.execute(statement)
        rows = result.all()

        posts = []
        for post, user, rating, comments_count in rows:
            is_favorited = False
            user_rating = None

            if current_user_id:
                try:
                    user_uuid = UUID(current_user_id)
                    is_favorited = await self._is_favorited(user_uuid, post.id)
                    user_rating = await self._get_user_rating(user_uuid, post.id)
                except ValueError:
                    pass

            posts.append(
                self._to_read(
                    post, user, rating or 0, user_rating, comments_count or 0, is_favorited
                )
            )

        return posts

    async def get_by_author(
        self, author_id: str, current_user_id: str | None = None
    ) -> list[PostRead]:
        try:
            author_uuid = UUID(author_id)
        except ValueError:
            return []

        statement = (
            select(
                PostORM,
                User,
                func.coalesce(func.sum(PostRating.value), 0).label("rating"),
                func.count(Comment.id.distinct()).label("comments_count"),
            )
            .join(User, PostORM.author_id == User.id)
            .outerjoin(PostRating, PostRating.post_id == PostORM.id)
            .outerjoin(Comment, Comment.post_id == PostORM.id)
            .where(PostORM.author_id == author_uuid)
            .group_by(PostORM.id, User.id)
            .order_by(PostORM.created_at.desc())
        )

        result = await self.session.execute(statement)
        rows = result.all()

        posts = []
        for post, user, rating, comments_count in rows:
            is_favorited = False
            user_rating = None

            if current_user_id:
                try:
                    user_uuid = UUID(current_user_id)
                    is_favorited = await self._is_favorited(user_uuid, post.id)
                    user_rating = await self._get_user_rating(user_uuid, post.id)
                except ValueError:
                    pass

            posts.append(
                self._to_read(
                    post, user, rating or 0, user_rating, comments_count or 0, is_favorited
                )
            )

        return posts

    async def create(self, post: PostCreate, author_id: str) -> PostRead:
        author_uuid = UUID(author_id)

        post_orm = PostORM(
            id=uuid4(),
            author_id=author_uuid,
            title=post.title,
            content=post.content,
            image_url=post.image_url,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(post_orm)
        await self.session.commit()
        await self.session.refresh(post_orm)

        user = await self.session.get(User, author_uuid)
        return self._to_read(post_orm, user, 0, None, 0, False)

    async def update(self, post_id: str, post: PostUpdate) -> PostRead | None:
        try:
            post_uuid = UUID(post_id)
        except ValueError:
            return None

        post_orm = await self.session.get(PostORM, post_uuid)
        if not post_orm:
            return None

        post_orm.title = post.title
        post_orm.content = post.content
        post_orm.updated_at = datetime.utcnow()

        self.session.add(post_orm)
        await self.session.commit()
        await self.session.refresh(post_orm)

        user = await self.session.get(User, post_orm.author_id)
        rating = await self._get_rating(post_uuid)
        comments_count = await self._get_comments_count(post_uuid)

        return self._to_read(post_orm, user, rating, None, comments_count, False)

    async def delete(self, post_id: str) -> bool:
        try:
            post_uuid = UUID(post_id)
        except ValueError:
            return False

        post = await self.session.get(PostORM, post_uuid)
        if not post:
            return False

        await self.session.delete(post)
        await self.session.commit()
        return True

    async def search(self, query: str, current_user_id: str | None = None) -> list[PostRead]:
        search_term = f"%{query}%"

        statement = (
            select(
                PostORM,
                User,
                func.coalesce(func.sum(PostRating.value), 0).label("rating"),
                func.count(Comment.id.distinct()).label("comments_count"),
            )
            .join(User, PostORM.author_id == User.id)
            .outerjoin(PostRating, PostRating.post_id == PostORM.id)
            .outerjoin(Comment, Comment.post_id == PostORM.id)
            .where(or_(PostORM.title.ilike(search_term), PostORM.content.ilike(search_term)))
            .group_by(PostORM.id, User.id)
            .order_by(PostORM.created_at.desc())
        )

        result = await self.session.execute(statement)
        rows = result.all()

        posts = []
        for post, user, rating, comments_count in rows:
            is_favorited = False
            user_rating = None

            if current_user_id:
                try:
                    user_uuid = UUID(current_user_id)
                    is_favorited = await self._is_favorited(user_uuid, post.id)
                    user_rating = await self._get_user_rating(user_uuid, post.id)
                except ValueError:
                    pass

            posts.append(
                self._to_read(
                    post, user, rating or 0, user_rating, comments_count or 0, is_favorited
                )
            )

        return posts

    async def _get_rating(self, post_id: UUID) -> int:
        result = await self.session.execute(
            select(func.coalesce(func.sum(PostRating.value), 0)).where(
                PostRating.post_id == post_id
            )
        )
        return result.scalar() or 0

    async def _get_comments_count(self, post_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(Comment.id)).where(Comment.post_id == post_id)
        )
        return result.scalar() or 0

    async def _is_favorited(self, user_id: UUID, post_id: UUID) -> bool:
        result = await self.session.execute(
            select(Favorite).where(Favorite.user_id == user_id, Favorite.post_id == post_id)
        )
        return result.scalar_one_or_none() is not None

    async def _get_user_rating(self, user_id: UUID, post_id: UUID) -> int | None:
        result = await self.session.execute(
            select(PostRating).where(PostRating.user_id == user_id, PostRating.post_id == post_id)
        )
        rating = result.scalar_one_or_none()
        return rating.value if rating else None

    @staticmethod
    def _to_read(
        post: PostORM,
        user: User | None,
        rating: int,
        user_rating: int | None,
        comments_count: int,
        is_favorited: bool,
    ) -> PostRead:
        return PostRead(
            id=str(post.id),
            authorId=str(post.author_id),
            authorLogin=user.login if user else None,
            authorAvatar=user.avatar_url if user else None,
            title=post.title,
            content=post.content,
            image_url=post.image_url,
            rating=rating,
            user_rating=user_rating,
            comments_count=comments_count,
            is_favorited=is_favorited,
            createdAt=post.created_at,
            updatedAt=post.updated_at,
        )


Post = PostORM
