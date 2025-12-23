from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.application.comments_service import CommentsService


@pytest.mark.asyncio
async def test_get_comments(mock_comment_repository, sample_post_id, sample_comment_read):
    service = CommentsService(mock_comment_repository)

    mock_comment_repository.get_by_post = AsyncMock(return_value=[sample_comment_read])

    results = await service.get_comments(sample_post_id)

    assert len(results) == 1
    mock_comment_repository.get_by_post.assert_called_once_with(sample_post_id)


@pytest.mark.asyncio
async def test_create_comment_success(
    mock_comment_repository, sample_post_id, sample_user_id, sample_comment_read
):
    service = CommentsService(mock_comment_repository)

    mock_comment_repository.create = AsyncMock(return_value=sample_comment_read)

    result = await service.create_comment(sample_post_id, sample_user_id, "Test comment")

    assert result.content == "Test comment"
    mock_comment_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_comment_empty_content(
    mock_comment_repository, sample_post_id, sample_user_id
):
    service = CommentsService(mock_comment_repository)

    with pytest.raises(HTTPException) as exc_info:
        await service.create_comment(sample_post_id, sample_user_id, "")

    assert exc_info.value.status_code == 400
    assert "cannot be empty" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_comment_whitespace_only(
    mock_comment_repository, sample_post_id, sample_user_id
):
    service = CommentsService(mock_comment_repository)

    with pytest.raises(HTTPException) as exc_info:
        await service.create_comment(sample_post_id, sample_user_id, "   ")

    assert exc_info.value.status_code == 400
    assert "cannot be empty" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_comment_success(mock_comment_repository, sample_comment_read, sample_user_id):
    service = CommentsService(mock_comment_repository)

    mock_comment_repository.get_by_id = AsyncMock(return_value=sample_comment_read)
    mock_comment_repository.delete = AsyncMock()

    await service.delete_comment(sample_comment_read.id, sample_user_id)

    mock_comment_repository.delete.assert_called_once_with(sample_comment_read.id)


@pytest.mark.asyncio
async def test_delete_comment_not_found(mock_comment_repository, sample_user_id):
    service = CommentsService(mock_comment_repository)

    mock_comment_repository.get_by_id = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_comment("nonexistent", sample_user_id)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_comment_not_author(mock_comment_repository, sample_comment_read):
    service = CommentsService(mock_comment_repository)

    other_user_id = sample_comment_read.authorId + "different"

    mock_comment_repository.get_by_id = AsyncMock(return_value=sample_comment_read)

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_comment(sample_comment_read.id, other_user_id)

    assert exc_info.value.status_code == 403
