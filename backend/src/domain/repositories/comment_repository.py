from abc import ABC, abstractmethod

from src.domain.models.posts import CommentCreate, CommentRead


class CommentRepository(ABC):
    @abstractmethod
    async def get_by_post(self, post_id: str) -> list[CommentRead]:
        pass

    @abstractmethod
    async def create(self, post_id: str, author_id: str, comment: CommentCreate) -> CommentRead:
        pass

    @abstractmethod
    async def delete(self, comment_id: str) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: str) -> CommentRead | None:
        pass
