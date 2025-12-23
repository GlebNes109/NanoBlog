from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.auth_service import AuthService
from src.application.comments_service import CommentsService
from src.application.favorites_service import FavoritesService
from src.application.posts_service import PostsService
from src.application.ratings_service import RatingsService
from src.application.uploads_service import UploadsService
from src.application.users_service import UsersService
from src.core.settings import settings
from src.domain.models.users import UserRead
from src.domain.password_hasher import PasswordHasher
from src.infrastructure.database.database import get_session
from src.infrastructure.password_hasher_impl import sha256HashCreator
from src.infrastructure.repositories.comment_repository_impl import CommentRepositoryImpl
from src.infrastructure.repositories.favorite_repository_impl import FavoriteRepositoryImpl
from src.infrastructure.repositories.post_repository_impl import PostRepositoryImpl
from src.infrastructure.repositories.rating_repository_impl import RatingRepositoryImpl
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


async def get_password_hasher() -> PasswordHasher:
    return sha256HashCreator()


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


async def get_post_repository(session: AsyncSession = Depends(get_session)) -> PostRepositoryImpl:
    return PostRepositoryImpl(session)


async def get_comment_repository(
    session: AsyncSession = Depends(get_session),
) -> CommentRepositoryImpl:
    return CommentRepositoryImpl(session)


async def get_favorite_repository(
    session: AsyncSession = Depends(get_session),
) -> FavoriteRepositoryImpl:
    return FavoriteRepositoryImpl(session)


async def get_rating_repository(
    session: AsyncSession = Depends(get_session),
) -> RatingRepositoryImpl:
    return RatingRepositoryImpl(session)


async def get_user_service(
    repo: UserRepositoryImpl = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> UsersService:
    return UsersService(repo, hasher)


async def get_auth_service(
    repo: UserRepositoryImpl = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthService:
    return AuthService(repo, hasher)


async def get_posts_service(
    repo: PostRepositoryImpl = Depends(get_post_repository),
) -> PostsService:
    return PostsService(repo)


async def get_comments_service(
    repo: CommentRepositoryImpl = Depends(get_comment_repository),
) -> CommentsService:
    return CommentsService(repo)


async def get_favorites_service(
    repo: FavoriteRepositoryImpl = Depends(get_favorite_repository),
) -> FavoritesService:
    return FavoritesService(repo)


async def get_ratings_service(
    repo: RatingRepositoryImpl = Depends(get_rating_repository),
) -> RatingsService:
    return RatingsService(repo)


async def get_uploads_service(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
) -> UploadsService:
    return UploadsService(user_repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepositoryImpl = Depends(get_user_repository),
) -> UserRead:
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
    except JWTError as err:
        raise credentials_exception from err

    user = await repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme_optional),
    repo: UserRepositoryImpl = Depends(get_user_repository),
) -> UserRead | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    return await repo.get_by_id(user_id)
