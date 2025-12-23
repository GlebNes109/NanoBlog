from fastapi import HTTPException, status

from src.domain.models.posts import PostRead
from src.domain.repositories.favorite_repository import FavoriteRepository


class FavoritesService:
    def __init__(self, repository: FavoriteRepository):
        self.repository = repository

    async def get_favorites(self, user_id: str) -> list[PostRead]:
        return await self.repository.get_user_favorites(user_id)

    async def add_to_favorites(self, user_id: str, post_id: str) -> None:
        added = await self.repository.add(user_id, post_id)
        if not added:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already in favorites or invalid post"
            )

    async def remove_from_favorites(self, user_id: str, post_id: str) -> None:
        removed = await self.repository.remove(user_id, post_id)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not in favorites"
            )


