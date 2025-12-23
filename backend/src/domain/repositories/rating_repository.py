from abc import ABC, abstractmethod


class RatingRepository(ABC):
    @abstractmethod
    async def get_post_rating(self, post_id: str) -> int:
        pass

    @abstractmethod
    async def get_user_rating(self, user_id: str, post_id: str) -> int | None:
        pass

    @abstractmethod
    async def set_rating(self, user_id: str, post_id: str, value: int) -> bool:
        pass

    @abstractmethod
    async def remove_rating(self, user_id: str, post_id: str) -> bool:
        pass


