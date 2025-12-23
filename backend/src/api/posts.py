from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user, get_current_user_optional, get_posts_service
from src.application.posts_service import PostsService
from src.domain.models.posts import PostCreateApi, PostRead, PostUpdate
from src.domain.models.users import UserRead

router = APIRouter()


@router.post("", summary="Создать пост", response_model=PostRead)
async def create_post(
    post: PostCreateApi,
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.create_post(post, current_user.id)


@router.get("/my", summary="Мои посты")
async def get_my_posts(
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.get_my_posts(current_user.id)


@router.get("", summary="Все посты")
async def get_posts(
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead | None = Depends(get_current_user_optional),
):
    user_id = current_user.id if current_user else None
    return await service.get_all_posts(user_id)


@router.get("/{post_id}", summary="Получить пост", response_model=PostRead)
async def get_post(
    post_id: str,
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead | None = Depends(get_current_user_optional),
):
    user_id = current_user.id if current_user else None
    return await service.get_post(post_id, user_id)


@router.put("/{post_id}", summary="Обновить пост")
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead = Depends(get_current_user),
):
    await service.update_post(post_id, post_data, current_user.id)
    return {"status": "updated"}


@router.delete("/{post_id}", summary="Удалить пост")
async def delete_post(
    post_id: str,
    service: PostsService = Depends(get_posts_service),
    current_user: UserRead = Depends(get_current_user),
):
    await service.delete_post(post_id, current_user.id)
    return {"status": "deleted"}
