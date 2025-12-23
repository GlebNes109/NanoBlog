from fastapi import APIRouter, Depends, Query

from src.api.dependencies import get_current_user_optional, get_posts_service, get_user_service
from src.application.posts_service import PostsService
from src.application.users_service import UsersService
from src.domain.models.users import UserRead

router = APIRouter()


@router.get("/posts", summary="Поиск постов")
async def search_posts(
    q: str = Query(..., min_length=1),
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead | None = Depends(get_current_user_optional),
):
    user_id = current_user.id if current_user else None
    return await service.search_posts(q, user_id)


@router.get("/users", summary="Поиск пользователей")
async def search_users(
    q: str = Query(..., min_length=1),
    service: UsersService = Depends(get_user_service),
):
    return await service.search_users(q)
