"""Unit tests for PostsService."""
import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock

from src.application.posts_service import PostsService
from src.domain.models.posts import PostCreateApi, PostUpdate


@pytest.mark.asyncio
async def test_create_post_success(mock_post_repository, sample_user_id, sample_post_read):
    """Test successful post creation."""
    service = PostsService(mock_post_repository)
    
    mock_post_repository.create = AsyncMock(return_value=sample_post_read)
    
    post_data = PostCreateApi(title="Test Post", content="Test content")
    
    result = await service.create_post(post_data, sample_user_id)
    
    assert result.title == "Test Post"
    mock_post_repository.create.assert_called_once()
    call_args = mock_post_repository.create.call_args
    assert call_args[0][1] == sample_user_id  # author_id


@pytest.mark.asyncio
async def test_get_post_success(mock_post_repository, sample_post_id, sample_post_read, sample_user_id):
    """Test successful post retrieval."""
    service = PostsService(mock_post_repository)
    
    mock_post_repository.get_by_id = AsyncMock(return_value=sample_post_read)
    
    result = await service.get_post(sample_post_id, sample_user_id)
    
    assert result.id == sample_post_id
    mock_post_repository.get_by_id.assert_called_once_with(sample_post_id, sample_user_id)


@pytest.mark.asyncio
async def test_get_post_not_found(mock_post_repository, sample_post_id):
    """Test post retrieval when post not found."""
    service = PostsService(mock_post_repository)
    
    mock_post_repository.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_post(sample_post_id)
    
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_all_posts(mock_post_repository, sample_post_read):
    """Test getting all posts."""
    service = PostsService(mock_post_repository)
    
    mock_post_repository.get_all = AsyncMock(return_value=[sample_post_read])
    
    results = await service.get_all_posts()
    
    assert len(results) == 1
    mock_post_repository.get_all.assert_called_once_with(None)


@pytest.mark.asyncio
async def test_update_post_success(
    mock_post_repository, sample_post_id, sample_user_id, sample_post_read
):
    """Test successful post update."""
    service = PostsService(mock_post_repository)
    
    updated_post_dict = sample_post_read.model_dump()
    updated_post_dict["title"] = "Updated title"
    updated_post = type(sample_post_read)(**updated_post_dict)
    
    mock_post_repository.get_by_id = AsyncMock(return_value=sample_post_read)
    mock_post_repository.update = AsyncMock(return_value=updated_post)
    
    post_update = PostUpdate(title="Updated title", content="Updated content")
    
    result = await service.update_post(sample_post_id, post_update, sample_user_id)
    
    assert result.title == "Updated title"
    mock_post_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_post_not_author(
    mock_post_repository, sample_post_id, sample_post_read
):
    """Test post update by non-author."""
    service = PostsService(mock_post_repository)
    
    other_user_id = sample_post_read.authorId + "different"
    
    mock_post_repository.get_by_id = AsyncMock(return_value=sample_post_read)
    
    post_update = PostUpdate(title="Updated title", content="Updated content")
    
    with pytest.raises(HTTPException) as exc_info:
        await service.update_post(sample_post_id, post_update, other_user_id)
    
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_delete_post_success(mock_post_repository, sample_post_id, sample_user_id, sample_post_read):
    """Test successful post deletion."""
    service = PostsService(mock_post_repository)
    
    mock_post_repository.get_by_id = AsyncMock(return_value=sample_post_read)
    mock_post_repository.delete = AsyncMock(return_value=True)
    
    await service.delete_post(sample_post_id, sample_user_id)
    
    mock_post_repository.delete.assert_called_once_with(sample_post_id)


@pytest.mark.asyncio
async def test_delete_post_not_author(mock_post_repository, sample_post_id, sample_post_read):
    """Test post deletion by non-author."""
    service = PostsService(mock_post_repository)
    
    other_user_id = sample_post_read.authorId + "different"
    
    mock_post_repository.get_by_id = AsyncMock(return_value=sample_post_read)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_post(sample_post_id, other_user_id)
    
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_search_posts(mock_post_repository, sample_post_read):
    """Test post search."""
    service = PostsService(mock_post_repository)
    
    mock_post_repository.search = AsyncMock(return_value=[sample_post_read])
    
    results = await service.search_posts("test")
    
    assert len(results) == 1
    mock_post_repository.search.assert_called_once_with("test", None)

