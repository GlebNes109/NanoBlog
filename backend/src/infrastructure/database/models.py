from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from collections.abc import Sequence


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    login: str = Field(unique=True, index=True)
    password_hash: str
    avatar_url: str | None = Field(default=None)
    bio: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    posts: list["Post"] = Relationship(back_populates="author")
    comments: list["Comment"] = Relationship(back_populates="author")
    favorites: list["Favorite"] = Relationship(back_populates="user")
    subscriptions_following: list["Subscription"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "Subscription.follower_id"},
    )
    subscriptions_followers: list["Subscription"] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "Subscription.following_id"},
    )


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="users.id", index=True)
    title: str
    content: str
    image_url: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    author: User = Relationship(back_populates="posts")
    tags: list["PostTag"] = Relationship(back_populates="post")
    comments: list["Comment"] = Relationship(back_populates="post")
    favorites: list["Favorite"] = Relationship(back_populates="post")
    ratings: list["PostRating"] = Relationship(back_populates="post")


class PostRating(SQLModel, table=True):
    __tablename__ = "post_ratings"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    post_id: UUID = Field(foreign_key="posts.id", primary_key=True)
    value: int = Field(ge=-1, le=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship()
    post: Post = Relationship(back_populates="ratings")


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)

    posts: list["PostTag"] = Relationship(back_populates="tag")


class PostTag(SQLModel, table=True):
    __tablename__ = "post_tags"

    post_id: UUID = Field(foreign_key="posts.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

    post: Post = Relationship(back_populates="tags")
    tag: Tag = Relationship(back_populates="posts")


class Favorite(SQLModel, table=True):
    __tablename__ = "favorites"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    post_id: UUID = Field(foreign_key="posts.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="favorites")
    post: Post = Relationship(back_populates="favorites")


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="posts.id", index=True)
    author_id: UUID = Field(foreign_key="users.id", index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    post: Post = Relationship(back_populates="comments")
    author: User = Relationship(back_populates="comments")


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    follower_id: UUID = Field(foreign_key="users.id", primary_key=True)
    following_id: UUID = Field(foreign_key="users.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    follower: User = Relationship(
        back_populates="subscriptions_following",
        sa_relationship_kwargs={"foreign_keys": "Subscription.follower_id"},
    )
    following: User = Relationship(
        back_populates="subscriptions_followers",
        sa_relationship_kwargs={"foreign_keys": "Subscription.following_id"},
    )

