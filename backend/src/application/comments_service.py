from fastapi import HTTPException, status

from src.domain.models.posts import CommentCreate, CommentRead
from src.domain.repositories.comment_repository import CommentRepository


class CommentsService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def get_comments(self, post_id: str) -> list[CommentRead]:
        return await self.repository.get_by_post(post_id)

    async def create_comment(self, post_id: str, author_id: str, content: str) -> CommentRead:
        if not content or not content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Comment content cannot be empty"
            )

        comment = CommentCreate(content=content.strip())
        return await self.repository.create(post_id, author_id, comment)

    async def delete_comment(self, comment_id: str, current_user_id: str) -> None:
        comment = await self.repository.get_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        if comment.authorId != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )

        await self.repository.delete(comment_id)
