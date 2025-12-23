from datetime import datetime

from pydantic import BaseModel


class PostRead(BaseModel):
    id: str
    authorId: str
    authorLogin: str | None = None
    authorAvatar: str | None = None
    title: str
    content: str
    image_url: str | None = None
    rating: int = 0
    user_rating: int | None = None
    comments_count: int = 0
    is_favorited: bool = False
    createdAt: datetime
    updatedAt: datetime


class PostCreate(BaseModel):
    title: str
    content: str
    image_url: str | None = None


class PostUpdate(BaseModel):
    title: str
    content: str


class PostCreateApi(BaseModel):
    title: str
    content: str


class CommentRead(BaseModel):
    id: str
    postId: str
    authorId: str
    authorLogin: str
    authorAvatar: str | None = None
    content: str
    createdAt: datetime


class CommentCreate(BaseModel):
    content: str


class RatingCreate(BaseModel):
    value: int  # -1, 0, 1
