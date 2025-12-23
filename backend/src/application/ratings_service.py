from fastapi import HTTPException, status

from src.domain.repositories.rating_repository import RatingRepository


class RatingsService:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    async def rate_post(self, user_id: str, post_id: str, value: int) -> dict:
        if value not in [-1, 0, 1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be -1, 0, or 1"
            )

        if value == 0:
            await self.repository.remove_rating(user_id, post_id)
            return {"status": "removed", "value": 0}

        await self.repository.set_rating(user_id, post_id, value)
        return {"status": "rated", "value": value}
