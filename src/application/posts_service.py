from datetime import datetime
import uuid

from starlette.responses import JSONResponse

from src.domain.models.posts import PostCreateApi, PostCreate, PostUpdate
from src.domain.post_repository import PostsRepository


class PostsService:
    def __init__(self, repository: PostsRepository):
        self.repository = repository

    async def create_post(self, post: PostCreateApi, author_id: str):
        post_create = PostCreate(
            title=post.title,
            content=post.content,
        )
        post_id = str(uuid.uuid4())
        return await self.repository.create(post_create, post_id, author_id)

    async def get_post(self, post_id: str, current_user_id: str):
        try:
            post = await self.repository.get(post_id)
        except KeyError:
            return JSONResponse(status_code=404, content=None)
        if post.authorId != current_user_id:
            return JSONResponse(status_code=403, content=None)
        return post

    async def get_my_posts(self, current_user_id: str):
        return await self.repository.get_all_by_author(current_user_id)

    async def get_all(self):
        return await self.repository.get_all()

    async def update_post(self, post_id: str, post: PostUpdate, current_user_id: str):
        try:
            existing = await self.repository.get(post_id)
        except KeyError:
            return JSONResponse(status_code=404, content=None)
        if existing.authorId != current_user_id:
            return JSONResponse(status_code=403, content=None)
        return await self.repository.update(post, post_id)

    async def delete_post(self, post_id: str, current_user_id: str):
        try:
            existing = await self.repository.get(post_id)
        except KeyError:
            return JSONResponse(status_code=404, content=None)
        if existing.authorId != current_user_id:
            return JSONResponse(status_code=403, content=None)
        if await self.repository.delete(post_id):
            return JSONResponse(status_code=204, content=None)


