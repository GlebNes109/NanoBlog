from datetime import datetime

from fastapi import HTTPException, status

from src.domain.models.users import UserCreate, UserPublic, UserProfileUpdate, UserCreateApi
from src.domain.password_hasher import PasswordHasher
from src.domain.repositories.user_repository import UserRepository


class UsersService:
    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher

    async def create_user(self, user: UserCreateApi) -> UserPublic:
        existing_email = await self.repository.get_by_email(user.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже зарегистрирован"
            )
        
        existing_login = await self.repository.get_by_login(user.login)
        if existing_login:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Логин уже занят"
            )
        
        hashed_password = await self.password_hasher.hash(user.password)
        user_create = UserCreate(
            email=user.email,
            login=user.login,
            password=hashed_password,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
        )
        user_read = await self.repository.create(user_create)
        return self._to_public(user_read)

    async def get_user(self, user_id: str) -> UserPublic:
        user = await self.repository.get_public_profile(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_my_profile(self, current_user_id: str) -> UserPublic:
        user = await self.repository.get_public_profile(current_user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_profile(self, user_id: str, profile: UserProfileUpdate) -> UserPublic:
        if profile.email:
            existing = await self.repository.get_by_email(profile.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email уже используется"
                )
        
        if profile.login:
            existing = await self.repository.get_by_login(profile.login)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Логин уже занят"
                )
        
        user = await self.repository.update_profile(user_id, profile)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def delete_user(self, user_id: str, current_user_id: str) -> None:
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not enough permissions"
            )
        
        deleted = await self.repository.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def search_users(self, query: str) -> list[UserPublic]:
        return await self.repository.search(query)

    @staticmethod
    def _to_public(user_read) -> UserPublic:
        return UserPublic(
            id=user_read.id,
            email=user_read.email,
            login=user_read.login,
            avatar_url=None,
            bio=None,
            createdAt=user_read.createdAt,
            updatedAt=user_read.updatedAt,
        )
