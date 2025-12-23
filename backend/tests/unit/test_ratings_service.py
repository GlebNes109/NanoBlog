from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.application.ratings_service import RatingsService


@pytest.mark.asyncio
async def test_rate_post_positive(mock_rating_repository, sample_user_id, sample_post_id):
    service = RatingsService(mock_rating_repository)

    mock_rating_repository.set_rating = AsyncMock()

    result = await service.rate_post(sample_user_id, sample_post_id, 1)

    assert result["status"] == "rated"
    assert result["value"] == 1
    mock_rating_repository.set_rating.assert_called_once_with(sample_user_id, sample_post_id, 1)


@pytest.mark.asyncio
async def test_rate_post_negative(mock_rating_repository, sample_user_id, sample_post_id):
    service = RatingsService(mock_rating_repository)

    mock_rating_repository.set_rating = AsyncMock()

    result = await service.rate_post(sample_user_id, sample_post_id, -1)

    assert result["status"] == "rated"
    assert result["value"] == -1
    mock_rating_repository.set_rating.assert_called_once_with(sample_user_id, sample_post_id, -1)


@pytest.mark.asyncio
async def test_remove_rating(mock_rating_repository, sample_user_id, sample_post_id):
    service = RatingsService(mock_rating_repository)

    mock_rating_repository.remove_rating = AsyncMock()

    result = await service.rate_post(sample_user_id, sample_post_id, 0)

    assert result["status"] == "removed"
    assert result["value"] == 0
    mock_rating_repository.remove_rating.assert_called_once_with(sample_user_id, sample_post_id)


@pytest.mark.asyncio
async def test_rate_post_invalid_value(mock_rating_repository, sample_user_id, sample_post_id):
    service = RatingsService(mock_rating_repository)

    with pytest.raises(HTTPException) as exc_info:
        await service.rate_post(sample_user_id, sample_post_id, 2)

    assert exc_info.value.status_code == 400
    assert "must be -1, 0, or 1" in exc_info.value.detail


@pytest.mark.asyncio
async def test_rate_post_invalid_negative_value(
    mock_rating_repository, sample_user_id, sample_post_id
):
    service = RatingsService(mock_rating_repository)

    with pytest.raises(HTTPException) as exc_info:
        await service.rate_post(sample_user_id, sample_post_id, -2)

    assert exc_info.value.status_code == 400
