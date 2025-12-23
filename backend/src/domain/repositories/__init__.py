from src.domain.repositories.base import BaseRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.post_repository import PostRepository
from src.domain.repositories.comment_repository import CommentRepository
from src.domain.repositories.favorite_repository import FavoriteRepository
from src.domain.repositories.rating_repository import RatingRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "PostRepository",
    "CommentRepository",
    "FavoriteRepository",
    "RatingRepository",
]


