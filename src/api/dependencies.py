from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.application.users_service import UsersService
from src.application.posts_service import PostsService
from src.core.settings import settings
from src.domain.models.users import UserRead
from src.domain.post_repository import PostsRepository
from src.domain.user_repository import UserRepository
from src.infrastructure.post_repository_impl import PostsRepositoryImpl
from src.infrastructure.simple_database import users as users_db
from src.infrastructure.user_repository_impl import UserRepositoryImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user_repository() -> UserRepositoryImpl:
    return UserRepositoryImpl()


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UsersService:
    return UsersService(repo)


def get_posts_repository() -> PostsRepositoryImpl:
    return PostsRepositoryImpl()


def get_posts_service(repo: PostsRepository = Depends(get_posts_repository)) -> PostsService:
    return PostsService(repo)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_db = users_db.get(user_id)
    if user_db is None:
        raise credentials_exception

    return UserRead(id=user_id, **user_db.model_dump())
