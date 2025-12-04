from datetime import datetime
from typing import Any

from src.domain.models.posts import PostCreate, PostDB, PostRead, PostUpdate
from src.domain.post_repository import PostsRepository
from src.infrastructure.simple_database import posts


class PostsRepositoryImpl(PostsRepository):
    async def get(self, id: Any) -> PostRead:
        return PostRead(id=id, **posts[str(id)].model_dump())

    async def get_all_by_author(self, author_id: Any) -> list[PostRead]:
        result: list[PostRead] = []
        for post_id, post in posts.items():
            if post is not None and post.authorId == str(author_id):
                result.append(PostRead(id=post_id, **post.model_dump()))
        return result

    async def create(self, obj: PostCreate, id: Any, author_id: Any) -> PostRead:
        posts[str(id)] = PostDB(
            authorId=str(author_id),
            title=obj.title,
            content=obj.content,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )
        return PostRead(id=id, **posts[str(id)].model_dump())

    async def update(self, obj: PostUpdate, id: Any) -> PostRead:
        existing = posts[str(id)]
        posts[str(id)] = PostDB(
            authorId=existing.authorId,
            title=obj.title,
            content=obj.content,
            createdAt=existing.createdAt,
            updatedAt=datetime.now(),
        )
        return PostRead(id=id, **posts[str(id)].model_dump())

    async def delete(self, id: Any) -> bool:
        posts[str(id)] = None
        return True

    async def get_all(self) -> list[PostRead]:
        result: list[PostRead] = []
        for post_id, post in posts.items():
            result.append(PostRead(id=post_id, **post.model_dump()))
        return result
