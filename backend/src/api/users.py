from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user, get_posts_service, get_user_service
from src.application.posts_service import PostsService
from src.application.users_service import UsersService
from src.domain.models.users import UserCreateApi, UserProfileUpdate, UserPublic, UserRead

router = APIRouter()


@router.post("", summary="Создать пользователя", response_model=UserPublic)
async def create_user(
    user: UserCreateApi,
    service: UsersService = Depends(get_user_service),
):
    return await service.create_user(user)


@router.get("/me", summary="Мой профиль", response_model=UserPublic)
async def get_my_profile(
    service: UsersService = Depends(get_user_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.get_my_profile(current_user.id)


@router.put("/me", summary="Обновить профиль", response_model=UserPublic)
async def update_my_profile(
    profile: UserProfileUpdate,
    service: UsersService = Depends(get_user_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.update_profile(current_user.id, profile)


@router.get("/{user_id}", summary="Получить пользователя", response_model=UserPublic)
async def get_user(
    user_id: str,
    service: UsersService = Depends(get_user_service),
):
    return await service.get_user(user_id)


@router.get("/{user_id}/posts", summary="Посты пользователя")
async def get_user_posts(
    user_id: str,
    posts_service: PostsService = Depends(get_posts_service),
):
    return await posts_service.get_user_posts(user_id)


@router.delete("/{user_id}", summary="Удаление профиля")
async def delete_user(
    user_id: str,
    service: UsersService = Depends(get_user_service),
    current_user: UserRead = Depends(get_current_user),
):
    await service.delete_user(user_id, current_user.id)
    return {"status": "deleted"}
