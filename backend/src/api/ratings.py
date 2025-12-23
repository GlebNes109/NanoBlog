from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user, get_ratings_service
from src.application.ratings_service import RatingsService
from src.domain.models.posts import RatingCreate
from src.domain.models.users import UserRead

router = APIRouter()


@router.post("/{post_id}/rate", summary="Оценить пост")
async def rate_post(
    post_id: str,
    rating: RatingCreate,
    service: RatingsService = Depends(get_ratings_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.rate_post(current_user.id, post_id, rating.value)
