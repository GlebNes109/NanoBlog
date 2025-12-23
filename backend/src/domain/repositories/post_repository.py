from abc import ABC, abstractmethod
from src.domain.models.posts import PostCreate, PostRead, PostUpdate


class PostRepository(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: str, current_user_id: str | None = None) -> PostRead | None:
        pass

    @abstractmethod
    async def get_all(self, current_user_id: str | None = None) -> list[PostRead]:
        pass

    @abstractmethod
    async def get_by_author(self, author_id: str, current_user_id: str | None = None) -> list[PostRead]:
        pass

    @abstractmethod
    async def create(self, post: PostCreate, author_id: str) -> PostRead:
        pass

    @abstractmethod
    async def update(self, post_id: str, post: PostUpdate) -> PostRead | None:
        pass

    @abstractmethod
    async def delete(self, post_id: str) -> bool:
        pass

    @abstractmethod
    async def search(self, query: str, current_user_id: str | None = None) -> list[PostRead]:
        pass


