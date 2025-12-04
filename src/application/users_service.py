import uuid
from datetime import datetime

from starlette.responses import JSONResponse

from src.domain.models.users import UserCreate
from src.domain.user_repository import UserRepository


class UsersService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user):
        id = str(uuid.uuid4())
        user_create = UserCreate(
            email=user.email,
            login=user.login,
            password=user.password,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        return await self.repository.create(user_create, id)

    async def get_user(self, user_id):
        try:
            return await self.repository.get(user_id)
        except KeyError:
            return JSONResponse(status_code=404, content=None)

    async def delete_user(self, user_id):
        if await self.repository.delete(user_id):
            return JSONResponse(status_code=204, content=None)

    async def update_user(self, user, user_id):
        try:
            return await self.repository.update(user, user_id)
        except KeyError:
            return JSONResponse(status_code=404, content=None)
