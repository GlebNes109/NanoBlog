from abc import ABC, abstractmethod

from src.domain.models.users import UserCreate, UserProfileUpdate, UserPublic, UserRead


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserRead | None:
        pass

    @abstractmethod
    async def get_by_login(self, login: str) -> UserRead | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserRead | None:
        pass

    @abstractmethod
    async def create(self, user: UserCreate) -> UserRead:
        pass

    @abstractmethod
    async def update_profile(self, user_id: str, profile: UserProfileUpdate) -> UserPublic | None:
        pass

    @abstractmethod
    async def update_avatar(self, user_id: str, avatar_url: str) -> bool:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def search(self, query: str) -> list[UserPublic]:
        pass

    @abstractmethod
    async def get_public_profile(self, user_id: str) -> UserPublic | None:
        pass
