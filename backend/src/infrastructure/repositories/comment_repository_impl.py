from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.models.posts import CommentRead, CommentCreate
from src.domain.repositories.comment_repository import CommentRepository
from src.infrastructure.database.models import Comment as CommentORM, User


class CommentRepositoryImpl(CommentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_post(self, post_id: str) -> list[CommentRead]:
        try:
            post_uuid = UUID(post_id)
        except ValueError:
            return []
        
        statement = (
            select(CommentORM, User)
            .join(User, CommentORM.author_id == User.id)
            .where(CommentORM.post_id == post_uuid)
            .order_by(CommentORM.created_at.desc())
        )
        
        result = await self.session.execute(statement)
        rows = result.all()
        
        return [self._to_read(comment, user) for comment, user in rows]

    async def create(self, post_id: str, author_id: str, comment: CommentCreate) -> CommentRead:
        post_uuid = UUID(post_id)
        author_uuid = UUID(author_id)
        
        comment_orm = CommentORM(
            id=uuid4(),
            post_id=post_uuid,
            author_id=author_uuid,
            content=comment.content,
        )
        self.session.add(comment_orm)
        await self.session.commit()
        await self.session.refresh(comment_orm)
        
        user = await self.session.get(User, author_uuid)
        return self._to_read(comment_orm, user)

    async def delete(self, comment_id: str) -> bool:
        try:
            comment_uuid = UUID(comment_id)
        except ValueError:
            return False
        
        comment = await self.session.get(CommentORM, comment_uuid)
        if not comment:
            return False
        
        await self.session.delete(comment)
        await self.session.commit()
        return True

    async def get_by_id(self, comment_id: str) -> CommentRead | None:
        try:
            comment_uuid = UUID(comment_id)
        except ValueError:
            return None
        
        comment = await self.session.get(CommentORM, comment_uuid)
        if not comment:
            return None
        
        user = await self.session.get(User, comment.author_id)
        return self._to_read(comment, user)

    @staticmethod
    def _to_read(comment: CommentORM, user: User | None) -> CommentRead:
        return CommentRead(
            id=str(comment.id),
            postId=str(comment.post_id),
            authorId=str(comment.author_id),
            authorLogin=user.login if user else "Unknown",
            authorAvatar=user.avatar_url if user else None,
            content=comment.content,
            createdAt=comment.created_at,
        )


