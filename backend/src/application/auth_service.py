from datetime import timedelta

from fastapi import HTTPException, status

from src.core.security import create_access_token
from src.core.settings import settings
from src.domain.password_hasher import PasswordHasher
from src.domain.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher

    async def login(self, username: str, password: str) -> dict:
        user = await self.repository.get_by_login(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
            )

        if not await self.password_hasher.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
            )

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires,
        )

        return {"access_token": access_token, "token_type": "bearer"}
