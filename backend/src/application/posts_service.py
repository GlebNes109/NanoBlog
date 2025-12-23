from fastapi import HTTPException, status

from src.domain.models.posts import PostCreate, PostRead, PostUpdate, PostCreateApi
from src.domain.repositories.post_repository import PostRepository


class PostsService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def create_post(self, post: PostCreateApi, author_id: str) -> PostRead:
        post_create = PostCreate(title=post.title, content=post.content)
        return await self.repository.create(post_create, author_id)

    async def get_post(self, post_id: str, current_user_id: str | None = None) -> PostRead:
        post = await self.repository.get_by_id(post_id, current_user_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    async def get_all_posts(self, current_user_id: str | None = None) -> list[PostRead]:
        return await self.repository.get_all(current_user_id)

    async def get_my_posts(self, author_id: str) -> list[PostRead]:
        return await self.repository.get_by_author(author_id, author_id)

    async def get_user_posts(self, author_id: str, current_user_id: str | None = None) -> list[PostRead]:
        return await self.repository.get_by_author(author_id, current_user_id)

    async def update_post(self, post_id: str, post_data: PostUpdate, current_user_id: str) -> PostRead:
        existing = await self.repository.get_by_id(post_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if existing.authorId != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
        updated = await self.repository.update(post_id, post_data)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return updated

    async def delete_post(self, post_id: str, current_user_id: str) -> None:
        existing = await self.repository.get_by_id(post_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if existing.authorId != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
        deleted = await self.repository.delete(post_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    async def search_posts(self, query: str, current_user_id: str | None = None) -> list[PostRead]:
        return await self.repository.search(query, current_user_id)
