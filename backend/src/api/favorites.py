from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user, get_favorites_service
from src.application.favorites_service import FavoritesService
from src.domain.models.users import UserRead

router = APIRouter()


@router.get("", summary="Избранные посты")
async def get_favorites(
    service: FavoritesService = Depends(get_favorites_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.get_favorites(current_user.id)


@router.post("/{post_id}", summary="Добавить в избранное")
async def add_to_favorites(
    post_id: str,
    service: FavoritesService = Depends(get_favorites_service),
    current_user: UserRead = Depends(get_current_user),
):
    await service.add_to_favorites(current_user.id, post_id)
    return {"status": "added"}


@router.delete("/{post_id}", summary="Удалить из избранного")
async def remove_from_favorites(
    post_id: str,
    service: FavoritesService = Depends(get_favorites_service),
    current_user: UserRead = Depends(get_current_user),
):
    await service.remove_from_favorites(current_user.id, post_id)
    return {"status": "removed"}
