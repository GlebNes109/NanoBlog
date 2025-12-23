from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")
CreateT = TypeVar("CreateT")
UpdateT = TypeVar("UpdateT")


class BaseRepository(ABC, Generic[T, CreateT, UpdateT]):
    @abstractmethod
    async def get(self, id: Any) -> T | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[T]:
        pass

    @abstractmethod
    async def create(self, obj: CreateT) -> T:
        pass

    @abstractmethod
    async def update(self, id: Any, obj: UpdateT) -> T | None:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        pass


