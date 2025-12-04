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
