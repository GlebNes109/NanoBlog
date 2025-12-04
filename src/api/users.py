from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_current_user, get_user_service
from src.application.users_service import UsersService
from src.domain.models.users import UserCreateApi, UserRead, UserUpdate

router = APIRouter()


@router.put("/{UserId}", summary="Изменение данных", description="Изменение данных юзера")
async def update_user(
    UserId: str,
    user: UserUpdate,
    service: UsersService = Depends(get_user_service),
    current_user: UserRead = Depends(get_current_user),
):
    if UserId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await service.update_user(user, UserId)


@router.delete("/{UserId}", summary="Удаление профиля", description="Удаление пользователя из бд")
async def delete_user(
    UserId: str,
    service: UsersService = Depends(get_user_service),
    current_user: UserRead = Depends(get_current_user),
):
    if UserId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await service.delete_user(UserId)


@router.post("")
async def create_user(user: UserCreateApi, service: UsersService = Depends(get_user_service)):
    return await service.create_user(user)


@router.get("/{UserId}")
async def get_user(
    UserId: str,
    service: UsersService = Depends(get_user_service),
    current_user: UserRead = Depends(get_current_user),
):
    if UserId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await service.get_user(UserId)
