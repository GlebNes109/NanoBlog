from abc import ABC, abstractmethod
from src.domain.models.posts import PostRead


class FavoriteRepository(ABC):
    @abstractmethod
    async def get_user_favorites(self, user_id: str) -> list[PostRead]:
        pass

    @abstractmethod
    async def add(self, user_id: str, post_id: str) -> bool:
        pass

    @abstractmethod
    async def remove(self, user_id: str, post_id: str) -> bool:
        pass

    @abstractmethod
    async def is_favorited(self, user_id: str, post_id: str) -> bool:
        pass


