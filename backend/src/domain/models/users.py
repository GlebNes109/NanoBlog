from datetime import datetime

from pydantic import BaseModel


class UserRead(BaseModel):
    id: str
    email: str
    login: str
    password: str
    createdAt: datetime  # Дата и время создания
    updatedAt: datetime  # Дата и время последнего редактирования


class UserCreate(BaseModel):
    email: str
    login: str
    password: str
    createdAt: datetime  # Дата и время создания
    updatedAt: datetime  # Дата и время последнего редактирования


class UserUpdate(BaseModel):
    email: str
    login: str
    password: str


class UserCreateApi(BaseModel):
    email: str
    login: str
    password: str


class UserDB(BaseModel):
    email: str
    login: str
    password: str
    createdAt: datetime  # Дата и время создания
    updatedAt: datetime  # Дата и время последнего редактирования


class UserPublic(BaseModel):
    id: str
    email: str
    login: str
    avatar_url: str | None = None
    bio: str | None = None
    createdAt: datetime
    updatedAt: datetime


class UserProfileUpdate(BaseModel):
    email: str | None = None
    login: str | None = None
    bio: str | None = None
