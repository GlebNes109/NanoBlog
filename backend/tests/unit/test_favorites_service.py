from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.application.favorites_service import FavoritesService


@pytest.mark.asyncio
async def test_get_favorites(mock_favorite_repository, sample_user_id, sample_post_read):
    service = FavoritesService(mock_favorite_repository)

    mock_favorite_repository.get_user_favorites = AsyncMock(return_value=[sample_post_read])

    results = await service.get_favorites(sample_user_id)

    assert len(results) == 1
    mock_favorite_repository.get_user_favorites.assert_called_once_with(sample_user_id)


@pytest.mark.asyncio
async def test_add_to_favorites_success(mock_favorite_repository, sample_user_id, sample_post_id):
    service = FavoritesService(mock_favorite_repository)

    mock_favorite_repository.add = AsyncMock(return_value=True)

    await service.add_to_favorites(sample_user_id, sample_post_id)

    mock_favorite_repository.add.assert_called_once_with(sample_user_id, sample_post_id)


@pytest.mark.asyncio
async def test_add_to_favorites_already_exists(
    mock_favorite_repository, sample_user_id, sample_post_id
):
    service = FavoritesService(mock_favorite_repository)

    mock_favorite_repository.add = AsyncMock(return_value=False)

    with pytest.raises(HTTPException) as exc_info:
        await service.add_to_favorites(sample_user_id, sample_post_id)

    assert exc_info.value.status_code == 400
    assert "Already in favorites" in exc_info.value.detail


@pytest.mark.asyncio
async def test_remove_from_favorites_success(
    mock_favorite_repository, sample_user_id, sample_post_id
):
    service = FavoritesService(mock_favorite_repository)

    mock_favorite_repository.remove = AsyncMock(return_value=True)

    await service.remove_from_favorites(sample_user_id, sample_post_id)

    mock_favorite_repository.remove.assert_called_once_with(sample_user_id, sample_post_id)


@pytest.mark.asyncio
async def test_remove_from_favorites_not_found(
    mock_favorite_repository, sample_user_id, sample_post_id
):
    service = FavoritesService(mock_favorite_repository)

    mock_favorite_repository.remove = AsyncMock(return_value=False)

    with pytest.raises(HTTPException) as exc_info:
        await service.remove_from_favorites(sample_user_id, sample_post_id)

    assert exc_info.value.status_code == 404
    assert "Not in favorites" in exc_info.value.detail
