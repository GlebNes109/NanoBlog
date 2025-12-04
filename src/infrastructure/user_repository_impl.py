from datetime import datetime
from typing import Any

from src.domain.user_repository import UserRepository
from src.domain.models.users import UserRead, UserCreate, UserUpdate, UserDB
from src.infrastructure.simple_database import users


class UserRepositoryImpl(UserRepository):
    async def get(self, id: Any) -> UserRead:
        return UserRead(id = id, **users[str(id)].model_dump())

    async def get_all(self) -> list[UserRead]:
        return users

    async def create(self, obj: UserCreate, id: Any) -> UserRead:
        users[str(id)] = UserDB(**obj.model_dump())
        return UserRead(id = id, **users[str(id)].model_dump())

    async def update(self, obj: UserUpdate, id: Any) -> UserRead:
        users[str(id)] = UserDB(email=obj.email,
                                login=obj.login,
                                password=obj.password,
                                createdAt=users[str(id)].createdAt,
                                updatedAt=datetime.now())
        return users[str(id)]

    async def delete(self, id: Any) -> bool:
        users[str(id)] = None
        return True