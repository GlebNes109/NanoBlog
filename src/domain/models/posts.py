from datetime import datetime

from pydantic import BaseModel


class PostRead(BaseModel):
    id: str
    authorId: str  # ID пользователя, создавшего пост
    title: str
    content: str
    createdAt: datetime  # Дата и время создания
    updatedAt: datetime  # Дата и время последнего редактирования


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str
    content: str


class PostCreateApi(BaseModel):
    title: str
    content: str


class PostDB(BaseModel):
    authorId: str  # ID пользователя, создавшего пост
    title: str
    content: str
    createdAt: datetime  # Дата и время создания
    updatedAt: datetime  # Дата и время последнего редактирования