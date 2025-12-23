from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user, get_comments_service
from src.application.comments_service import CommentsService
from src.domain.models.posts import CommentRead, CommentCreate
from src.domain.models.users import UserRead

router = APIRouter()


@router.get("/{post_id}/comments", summary="Комментарии к посту")
async def get_comments(
    post_id: str,
    service: CommentsService = Depends(get_comments_service),
) -> list[CommentRead]:
    return await service.get_comments(post_id)


@router.post("/{post_id}/comments", summary="Добавить комментарий", response_model=CommentRead)
async def create_comment(
    post_id: str,
    comment: CommentCreate,
    service: CommentsService = Depends(get_comments_service),
    current_user: UserRead = Depends(get_current_user),
):
    return await service.create_comment(post_id, current_user.id, comment.content)


@router.delete("/{post_id}/comments/{comment_id}", summary="Удалить комментарий")
async def delete_comment(
    post_id: str,
    comment_id: str,
    service: CommentsService = Depends(get_comments_service),
    current_user: UserRead = Depends(get_current_user),
):
    await service.delete_comment(comment_id, current_user.id)
    return {"status": "deleted"}
